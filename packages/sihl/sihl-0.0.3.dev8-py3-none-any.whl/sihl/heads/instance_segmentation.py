from __future__ import annotations

from typing import Any, Callable

from torch import Tensor
from torch.nn import functional as F
from torch.nn.functional import interpolate
from torchmetrics.detection.mean_ap import MeanAveragePrecision
from torchvision.ops import box_iou, complete_box_iou_loss, nms
from torchvision.utils import draw_segmentation_masks, masks_to_boxes
import torch
import torch.nn as nn

from sihl.layers import SequentialConvBlocks, BilinearUpscaler
from sihl.utils import (
    get_coordinate_grid,
    get_relative_coordinate_grid,
    get_func_locals_and_return,
    init_weights,
    soft_dice_loss,
)


def f_beta(beta: float) -> Callable[[Tensor, Tensor], Tensor]:
    """F-beta score second order function."""
    return lambda p, r: (1 + beta**2) * p * r / (beta**2 * p + r)


class UpscaleAddFusion(nn.Module):
    """
    Upscale all inputs at levels `min_level + 1` to `max_level` to the same resolution
    as the input at `min_level`.
    """

    def __init__(self, min_level: int, max_level: int):
        assert max_level > min_level
        self.min_level, self.max_level = min_level, max_level
        num_levels = max_level - min_level + 1
        self.upscalers = nn.ModuleList(
            [BilinearUpscaler(scale=2**_) for _ in range(1, num_levels)]
        )

    def forward(self, inputs: list[Tensor]) -> Tensor:
        output = inputs[self.min_level]
        for level, upscaler in zip(
            range(self.min_level + 1, self.max_level + 1), self.upscalers
        ):
            output = output + upscaler(inputs[level])
        return output


class InstanceSegmentation(nn.Module):
    """Instance segmentation head based on CondInst and the TAL from TOOD.

    References:
        [1] [TOOD](https://arxiv.org/abs/2108.07755)
        [2] [CondInst](https://arxiv.org/abs/2102.03026)
    """

    def __init__(  # noqa: D107
        self,
        in_channels: list[int],
        num_classes: int,
        num_channels: int = 256,
        mask_num_channels: int = 128,
        num_layers: int = 4,
        min_level: int = 3,
        max_level: int = 7,
        nms_threshold: float = 0.6,
        max_instances: int = 100,
        class_names: list[str] | None = None,
    ):
        super().__init__()
        assert all(
            _ == in_channels[min_level] for _ in in_channels[min_level : max_level + 1]
        )
        self.num_classes = num_classes
        self.class_names = class_names or tuple(str(_) for _ in range(num_classes))
        self.nms_threshold = nms_threshold
        self.max_instances = max_instances
        self.min_level = min_level
        self.max_level = max_level
        self.pre_nms_score_threshold = 0.05
        self.box_weight = 2.0
        self.mask_weight = 1.0
        input_channels = in_channels[min_level]
        self.class_head = SequentialConvBlocks(
            input_channels, num_channels, num_layers=num_layers, norm="group"
        )
        self.class_head.append(nn.Conv2d(num_channels, num_classes, 3, padding=1))
        self.box_head = SequentialConvBlocks(
            input_channels, num_channels, num_layers=num_layers, norm="group"
        )
        self.box_head.append(nn.Conv2d(num_channels, 4, 3, padding=1))
        self.box_head.append(nn.ReLU())
        self.controller_head = SequentialConvBlocks(
            input_channels, num_channels, num_layers=num_layers, norm="group"
        )
        self.controller_head.append(nn.Conv2d(num_channels, 169, 3, padding=1))
        self.bottom_module = SequentialConvBlocks(
            input_channels, mask_num_channels, num_layers=3, norm="group"
        )
        self.bottom_module.append(nn.Conv2d(mask_num_channels, 8, 3, padding=1))
        self.bottom_fusion = UpscaleAddFusion(min_level=min_level, max_level=5)
        self.apply(init_weights)
        self.tal_alpha, self.tal_beta, self.tal_topk, self.loss_gamma = 1, 6, 13, 2
        self.register_buffer("thresh", torch.tensor(0.5))
        self.register_buffer("signs", torch.tensor([-1, -1, 1, 1]).reshape(1, 1, 4))
        self.output_shapes = {
            "num_instances": ("batch_size",),
            "scores": ("batch_size", max_instances),
            "classes": ("batch_size", max_instances),
            "boxes": ("batch_size", max_instances, 4),
        }

    def forward_single_level(
        self, input: Tensor, level: int
    ) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        """Forward pass for a single level.

        Args:
            input (Tensor): Level features
            level (int): Level index

        Returns:
            tuple[Tensor, Tensor]: Prediction logits and boxes
        """
        stride, (h, w), device = 2**level, input.shape[2:], input.device
        y_max, x_max = h * stride, w * stride
        centers = get_coordinate_grid(h, w, y_max, x_max)
        centers = centers.to(device).flatten(1, 2).transpose(0, 1)  # (I, 2)
        pred_boxes = centers.repeat(1, 2) + self.signs.to(device) * (
            stride * self.box_head(input).flatten(2, 3).transpose(1, 2) + 1
        )
        logits = self.class_head(input).flatten(2, 3).transpose(1, 2)
        dynamic_params = self.controller_head(input).flatten(2, 3).transpose(1, 2)
        centers[:, 0] = centers[:, 0] / x_max
        centers[:, 1] = centers[:, 1] / y_max
        return logits, pred_boxes, centers, dynamic_params

    def forward_multi_level(
        self, inputs: list[Tensor]
    ) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        """Forward pass for multiple levels.

        Args:
            inputs (list[Tensor]): Input features by level

        Returns:
            tuple[Tensor, Tensor]: Prediction logits and boxes
        """
        level_outputs = [
            self.forward_single_level(inputs[level], level)
            for level in range(self.min_level, self.max_level + 1)
        ]
        logits = torch.cat([_[0] for _ in level_outputs], dim=1)
        pred_boxes = torch.cat([_[1] for _ in level_outputs], dim=1)
        centers = torch.cat([_[2] for _ in level_outputs], dim=1)
        dynamic_params = torch.cat([_[3] for _ in level_outputs], dim=1)
        return logits, pred_boxes, centers, dynamic_params

    @staticmethod
    def compute_segmentation_mask(
        f_bottom: Tensor, center: Tensor, params: Tensor
    ) -> Tensor:
        rel_coords = get_relative_coordinate_grid(
            height=f_bottom.shape[1],
            width=f_bottom.shape[2],
            x=center[0].item() * f_bottom.shape[2],
            y=center[1].item() * f_bottom.shape[1],
        ).to(f_bottom.device)
        x = torch.cat([rel_coords.to(f_bottom.dtype), f_bottom]).unsqueeze(0)
        # FIXME: parametrize magic numbers
        w1, b1 = params[:80].reshape(8, 10, 1, 1), params[80:88]
        w2, b2 = params[88:152].reshape(8, 8, 1, 1), params[152:160]
        w3, b3 = params[160:168].reshape(1, 8, 1, 1), params[168:169]
        x = F.conv2d(F.conv2d(F.conv2d(x, w1, b1).relu(), w2, b2).relu(), w3, b3)
        return x.sigmoid().squeeze(0, 1)

    def forward(self, inputs: list[Tensor]) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        """Prediction forward pass.

        Args:
            inputs (list[Tensor]): Input features by level

        Returns:
            tuple[Tensor, Tensor, Tensor, Tensor]: Prediction instances, scores, classes
                and segmentation masks
        """
        f_bottom = self.bottom_fusion(inputs)
        logits, pred_boxes, centers, dynamic_params = self.forward_multi_level(inputs)
        pred_scores = torch.sigmoid(logits)
        pred_scores, pred_classes = pred_scores.max(dim=2)
        batch_size, device = inputs[0].shape[0], inputs[0].device
        filtered_shape = (batch_size, self.max_instances)
        num_instances = torch.zeros((batch_size,), dtype=torch.int64, device=device)
        filtered_scores = torch.zeros(filtered_shape, device=device)
        filtered_classes = torch.zeros(filtered_shape, dtype=torch.int64, device=device)
        filtered_centers = torch.zeros(filtered_shape + (2,), device=device)
        filtered_dynamic_params = torch.zeros(
            filtered_shape + (dynamic_params.shape[-1],), device=device
        )
        masks = torch.zeros(filtered_shape + tuple(f_bottom.shape[2:]), device=device)
        for batch in range(batch_size):
            postitive_mask = pred_scores[batch] > self.pre_nms_score_threshold
            masked_score = pred_scores[batch, postitive_mask]
            masked_box = pred_boxes[batch, postitive_mask]
            masked_centers = centers[batch, postitive_mask]
            masked_dynamic_params = dynamic_params[batch, postitive_mask]
            nms_idxs = nms(masked_box, masked_score, self.nms_threshold)
            nms_idxs = nms_idxs[: self.max_instances]
            n = nms_idxs.shape[0]
            num_instances[batch] = (masked_score[nms_idxs] > self.thresh).float().sum()
            filtered_scores[batch, :n] = masked_score[nms_idxs]
            filtered_classes[batch, :n] = pred_classes[batch, postitive_mask][nms_idxs]
            filtered_centers[batch, :n] = masked_centers[nms_idxs]
            filtered_dynamic_params[batch, :n] = masked_dynamic_params[nms_idxs]
            # FIXME: use grouped convolutions instead of for-loop to speed things up
            for idx, (center, params) in enumerate(
                zip(filtered_centers[batch, :n], filtered_dynamic_params[batch, :n])
            ):
                masks[batch, idx, :, :] = self.compute_segmentation_mask(
                    f_bottom[batch], center, params
                )
        return num_instances, filtered_scores, filtered_classes, masks

    @torch.no_grad()
    def get_targets(
        self,
        inputs: list[Tensor],
        gt_classes: list[Tensor],
        gt_boxes: list[Tensor],
        pred_scores: Tensor,
        pred_boxes: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        """Get target tensors for loss computations.

        Args:
            inputs (list[Tensor]): Input features by level
            gt_classes (list[Tensor]): Ground truth classes by sample in mini-batch
            gt_boxes (list[Tensor]): Ground truth boxes by sample in mini-batch
            pred_scores (Tensor): Prediction scores
            pred_boxes (Tensor): Prediction boxes

        Returns:
            tuple[Tensor, Tensor, Tensor]: Target scores, indices, and weights
        """
        batch_size, device = inputs[0].shape[0], inputs[0].device
        target_scores = torch.zeros_like(pred_scores, device=device)
        target_indices = torch.zeros(
            pred_boxes.shape[:2], dtype=torch.int64, device=device
        )
        target_weights = torch.zeros(pred_boxes.shape[:2], device=device)
        box_area = torch.zeros(pred_boxes.shape[:2], device=device)
        centers_list = []
        for level in range(self.min_level, self.max_level + 1):
            input = inputs[level]
            stride, (height, width) = 2**level, input.shape[2:]
            y_max, x_max = height * stride, width * stride
            grid = get_coordinate_grid(height, width, y_max, x_max).to(device)
            centers_list.append(grid.reshape(2, -1))
        centers = torch.cat(centers_list, dim=1)
        for batch in range(batch_size):
            if gt_boxes[batch].shape[0] == 0:
                continue
            batch_ious = box_iou(gt_boxes[batch], pred_boxes[batch])
            for gt_idx, (gt_box, gt_class) in enumerate(
                zip(gt_boxes[batch], gt_classes[batch])
            ):
                gt_w, gt_h = gt_box[2] - gt_box[0], gt_box[3] - gt_box[1]
                pos_mask = torch.ones(centers.shape[1], dtype=torch.bool, device=device)
                pos_mask &= (centers[0] > gt_box[0]) & (centers[0] < gt_box[2])
                pos_mask &= (centers[1] > gt_box[1]) & (centers[1] < gt_box[3])
                scores = pred_scores[batch, :, gt_class]
                ious = batch_ious[gt_idx] * pos_mask.float()
                alignment = scores**self.tal_alpha * ious**self.tal_beta
                alignment = alignment * ious.max() / alignment.max()
                _, positive_idxs = alignment.topk(self.tal_topk)
                positive_idxs = positive_idxs[alignment[positive_idxs] > 0]
                for pos_idx in positive_idxs:
                    old_area, new_area = box_area[batch, pos_idx], gt_h * gt_w
                    if old_area > 0 and old_area < new_area:
                        continue
                    target_scores[batch, pos_idx, gt_class] = alignment[pos_idx]
                    target_indices[batch, pos_idx] = gt_idx
                    target_weights[batch, pos_idx] = alignment[pos_idx]
                    box_area[batch, pos_idx] = new_area
        return target_scores, target_indices, target_weights

    def training_step(
        self, inputs: list[Tensor], classes: list[Tensor], masks: list[Tensor]
    ) -> tuple[Tensor, dict[str, Any]]:
        """Perform single training step.

        Args:
            inputs (list[Tensor]): Input features by level
            classes (list[Tensor]): Ground truth classes by sample in mini-batch
            masks (list[Tensor]): Ground truth masks (NHW) by sample in mini-batch

        Returns:
            tuple[Tensor, dict[str, Any]]: Total and partial or auxiliary losses
        """
        logits, pred_boxes, centers, dynamic_params = self.forward_multi_level(inputs)
        pred_scores = torch.sigmoid(logits)
        gt_boxes = [masks_to_boxes(sample_masks) for sample_masks in masks]
        target_scores, target_indices, target_weights = self.get_targets(
            inputs, classes, gt_boxes, pred_scores, pred_boxes
        )

        class_loss = (
            torch.nn.functional.binary_cross_entropy_with_logits(
                logits, target_scores, reduction="none"
            )
            * (pred_scores - target_scores).abs() ** self.loss_gamma
        ).sum() / target_scores.sum()

        positive_idxs_2d = torch.nonzero(target_weights)
        positive_idxs_flat = torch.nonzero(target_weights.flatten()).squeeze()
        pred_boxes = torch.stack(
            [pred_boxes[batch, idx] for (batch, idx) in positive_idxs_2d]
        )
        target_boxes = torch.stack(
            [gt_boxes[batch][idx] for (batch, idx) in positive_idxs_2d]
        )
        box_loss = (
            complete_box_iou_loss(pred_boxes, target_boxes, reduction="none")
            * target_weights.flatten()[positive_idxs_flat]
        ).sum() / target_scores.sum()
        f_bottom = self.bottom_fusion(inputs)
        pred_masks = torch.stack(
            [
                self.compute_segmentation_mask(
                    f_bottom[batch], centers[batch, idx], dynamic_params[batch, idx]
                )
                for (batch, idx) in positive_idxs_2d
            ]
        )
        # resize ground truth masks to match prediction masks' resolution
        masks = [
            interpolate(
                mask.unsqueeze(0),
                size=tuple(inputs[self.min_level].shape[2:]),
                mode="bilinear",
            ).squeeze(0)
            for mask in masks
        ]
        target_masks = torch.stack(
            [masks[batch][idx] for (batch, idx) in positive_idxs_2d]
        )
        mask_loss = soft_dice_loss(pred_masks, target_masks)
        loss = class_loss + self.box_weight * box_loss + self.mask_weight * mask_loss
        return loss, {
            "class_loss": class_loss.detach(),
            "box_loss": box_loss.detach(),
            "mask_loss": mask_loss.detach(),
        }

    @torch.no_grad()
    def on_validation_start(self) -> None:
        """(Re)Set mAP computer for the validation epoch."""
        self.map_computer = MeanAveragePrecision(iou_type="segm")

    @torch.no_grad()
    def validation_step(
        self, inputs: list[Tensor], classes: list[Tensor], masks: list[Tensor]
    ) -> tuple[Tensor, dict[str, Any]]:
        """Perform single validation step.

        Args:
            inputs (list[Tensor]): Input features by level
            classes (list[Tensor]): Ground truth classes by sample in mini-batch
            bboxes (list[Tensor]): Ground truth boxes by sample in mini-batch

        Returns:
            tuple[Tensor, dict[str, Any]]: Total and partial or auxiliary losses
        """
        num_instances, scores, pred_classes, pred_masks = self.forward(inputs)
        self.map_computer.update(
            [
                {"scores": s, "labels": c, "masks": m}
                for n, s, c, m in zip(num_instances, scores, pred_classes, pred_masks)
            ],
            [{"labels": c, "masks": m} for c, m in zip(classes, masks)],
        )
        return self.training_step(inputs, classes, masks)

    @torch.no_grad()
    def on_validation_end(self) -> dict[str, Any]:
        """Compute validation epoch metrics."""
        aggregated_metrics: dict[str, Any] = self.map_computer.compute()
        del aggregated_metrics["map_per_class"]
        del aggregated_metrics["mar_100_per_class"]
        f_locals, (precision, recall) = get_func_locals_and_return(
            self.map_computer._calculate, self.map_computer._get_classes()
        )
        scores = f_locals["scores"]
        precision = precision[0, :, :, 0, 2].mean(dim=1)
        recall = torch.linspace(0.0, 1.0, round(1.0 / 0.01) + 1)
        scores = scores[0, :, :, 0, 2].mean(dim=1)
        f1 = f_beta(1.0)(precision, recall)
        f0_5 = f_beta(0.5)(precision, recall)
        f2 = f_beta(2.0)(precision, recall)
        # automatically choose the threshold which gives the best F-score
        best_idx = int(f1.argmax().item())
        aggregated_metrics["threshold"] = scores[best_idx]
        self.thresh = aggregated_metrics["threshold"]
        aggregated_metrics["precision"] = precision[best_idx]
        aggregated_metrics["recall"] = recall[best_idx]
        aggregated_metrics["f1"] = f1[best_idx]
        aggregated_metrics["f0.5"] = f0_5[best_idx]
        aggregated_metrics["f2"] = f2[best_idx]
        return aggregated_metrics

    def visualize(
        self, inputs: list[Tensor], classes: list[Tensor], masks: list[Tensor]
    ) -> list[Tensor]:
        num_instances, scores, pred_classes, pred_masks = self.forward(inputs)
        visualizations: list[Tensor] = []
        for batch, image in enumerate(inputs[0]):
            image = draw_segmentation_masks(
                (image * 255).to(torch.uint8), masks[batch], colors="yellow"
            )
            visualizations.append(
                draw_segmentation_masks(
                    image, pred_masks[batch][: num_instances[batch]], colors="blue"
                )
            )
        return visualizations
