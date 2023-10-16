from __future__ import annotations

try:
    from importlib_resources import as_file, files
except ImportError:
    from importlib.resources import files, as_file  # type: ignore

from typing import Any, Callable

import torch
import torch.nn as nn
from torch import Tensor
from torchmetrics.detection.mean_ap import MeanAveragePrecision
from torchvision.ops import box_iou, complete_box_iou_loss, nms
from torchvision.utils import draw_bounding_boxes

from sihl.layers import SequentialConvBlocks
from sihl.utils import get_coordinate_grid, get_func_locals_and_return, init_weights


def f_beta(beta: float) -> Callable[[Tensor, Tensor], Tensor]:
    """F-beta score second order function."""
    return lambda p, r: (1 + beta**2) * p * r / (beta**2 * p + r)


class ObjectDetection(nn.Module):
    """Object detection head based on FCOS and TOOD.

    References:
        [1] [FCOS](https://arxiv.org/abs/1904.01355)
        [2] [TOOD](https://arxiv.org/abs/2108.07755)
    """

    def __init__(  # noqa: D107
        self,
        in_channels: list[int],
        num_classes: int,
        num_channels: int = 256,
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
        self.box_loss_weight = 2.0
        self.class_head = SequentialConvBlocks(
            in_channels[min_level], num_channels, num_layers=num_layers, norm="group"
        )
        self.class_head.append(nn.Conv2d(num_channels, num_classes, 3, padding=1))
        self.box_head = SequentialConvBlocks(
            in_channels[min_level], num_channels, num_layers=num_layers, norm="group"
        )
        self.box_head.append(nn.Conv2d(num_channels, 4, 3, padding=1))
        self.box_head.append(nn.ReLU())
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

    def forward_single_level(self, input: Tensor, level: int) -> tuple[Tensor, Tensor]:
        """Forward pass for a single level.

        Args:
            input (Tensor): Level features
            level (int): Level index

        Returns:
            tuple[Tensor, Tensor]: Prediction logits and boxes
        """
        stride, (h, w), device = 2**level, input.shape[2:], input.device
        y_max, x_max = h * stride, w * stride
        grid = get_coordinate_grid(h, w, y_max, x_max).to(device).flatten(1, 2)
        pred_boxes = grid.repeat(2, 1).transpose(0, 1) + self.signs.to(device) * (
            stride * self.box_head(input).flatten(2, 3).transpose(1, 2) + 1
        )
        pred_logits = self.class_head(input).flatten(2, 3).transpose(1, 2)
        return pred_logits, pred_boxes  # (B, I, K), (B, I, 4)

    def forward_multi_level(self, inputs: list[Tensor]) -> tuple[Tensor, Tensor]:
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
        multi_level_pred_logits = torch.cat([_[0] for _ in level_outputs], dim=1)
        multi_level_pred_boxes = torch.cat([_[1] for _ in level_outputs], dim=1)
        return multi_level_pred_logits, multi_level_pred_boxes  # (B, I, K), (B, I, 4)

    def forward(self, inputs: list[Tensor]) -> tuple[Tensor, Tensor, Tensor, Tensor]:
        """Prediction forward pass.

        Args:
            inputs (list[Tensor]): Input features by level

        Returns:
            tuple[Tensor, Tensor, Tensor, Tensor]: Prediction instances, scores, classes
                and boxes
        """
        pred_logits, pred_boxes = self.forward_multi_level(inputs)
        pred_scores = torch.sigmoid(pred_logits)
        pred_scores, pred_classes = pred_scores.max(dim=2)
        batch_size, device = inputs[0].shape[0], inputs[0].device
        filtered_shape = (batch_size, self.max_instances)
        num_instances = torch.zeros((batch_size,), dtype=torch.int64, device=device)
        filtered_scores = torch.zeros(filtered_shape, device=device)
        filtered_classes = torch.zeros(filtered_shape, dtype=torch.int64, device=device)
        filtered_boxes = torch.zeros(filtered_shape + (4,), device=device)
        for batch in range(batch_size):
            mask = pred_scores[batch] > self.pre_nms_score_threshold
            masked_score, masked_box = pred_scores[batch, mask], pred_boxes[batch, mask]
            nms_idxs = nms(masked_box, masked_score, self.nms_threshold)
            nms_idxs = nms_idxs[: self.max_instances]
            n = nms_idxs.shape[0]
            num_instances[batch] = (masked_score[nms_idxs] > self.thresh).float().sum()
            filtered_scores[batch, :n] = masked_score[nms_idxs]
            filtered_classes[batch, :n] = pred_classes[batch, mask][nms_idxs]
            filtered_boxes[batch, :n] = masked_box[nms_idxs]
        return num_instances, filtered_scores, filtered_classes, filtered_boxes

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
            tuple[Tensor, Tensor, Tensor]: Target scores, boxes, and weights
        """
        batch_size, device = inputs[0].shape[0], inputs[0].device
        target_scores = torch.zeros_like(pred_scores, device=device)
        target_boxes = torch.zeros_like(pred_boxes, device=device)
        box_weight = torch.zeros(pred_boxes.shape[:2], device=device)
        box_area = torch.zeros(pred_boxes.shape[:2], device=device)
        centers_list = []
        for level in range(self.min_level, self.max_level + 1):
            input = inputs[level]
            stride, (height, width) = 2**level, input.shape[2:]
            max_y, max_x = height * stride, width * stride
            grid = get_coordinate_grid(height, width, max_y, max_x).to(device)
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
                mask = torch.ones(centers.shape[1], dtype=torch.bool, device=device)
                mask &= (centers[0] > gt_box[0]) & (centers[0] < gt_box[2])
                mask &= (centers[1] > gt_box[1]) & (centers[1] < gt_box[3])
                scores = pred_scores[batch, :, gt_class]
                ious = batch_ious[gt_idx] * mask.float()
                alignment = scores**self.tal_alpha * ious**self.tal_beta
                alignment = alignment * ious.max() / alignment.max()
                _, positive_idxs = alignment.topk(self.tal_topk)
                positive_idxs = positive_idxs[alignment[positive_idxs] > 0]
                for pos_idx in positive_idxs:
                    old_area, new_area = box_area[batch, pos_idx], gt_h * gt_w
                    if old_area > 0 and old_area < new_area:
                        continue
                    target_scores[batch, pos_idx, gt_class] = alignment[pos_idx]
                    target_boxes[batch, pos_idx] = gt_box
                    box_weight[batch, pos_idx] = alignment[pos_idx]
                    box_area[batch, pos_idx] = new_area
        return target_scores, target_boxes, box_weight

    def training_step(
        self, inputs: list[Tensor], classes: list[Tensor], boxes: list[Tensor]
    ) -> tuple[Tensor, dict[str, Any]]:
        """Perform single training step.

        Args:
            inputs (list[Tensor]): Input features by level
            classes (list[Tensor]): Ground truth classes by sample in mini-batch
            bboxes (list[Tensor]): Ground truth boxes by sample in mini-batch

        Returns:
            tuple[Tensor, dict[str, Any]]: Total and partial or auxiliary losses
        """
        pred_logits, pred_boxes = self.forward_multi_level(inputs)
        pred_scores = torch.sigmoid(pred_logits)
        target_scores, target_boxes, box_weight = self.get_targets(
            inputs, classes, boxes, pred_scores, pred_boxes
        )
        class_loss = (
            torch.nn.functional.binary_cross_entropy_with_logits(
                pred_logits, target_scores, reduction="none"
            )
            * (pred_scores - target_scores).abs() ** self.loss_gamma
        ).sum() / target_scores.sum()
        box_idxs = torch.nonzero(box_weight.flatten()).squeeze()
        box_loss = (
            complete_box_iou_loss(
                pred_boxes.flatten(0, 1)[box_idxs],
                target_boxes.flatten(0, 1)[box_idxs],
                reduction="none",
            )
            * box_weight.flatten()[box_idxs]
        ).sum() / target_scores.sum()
        loss = class_loss + self.box_loss_weight * box_loss
        return loss, {"class_loss": class_loss.detach(), "box_loss": box_loss.detach()}

    @torch.no_grad()
    def on_validation_start(self) -> None:
        """(Re)Set mAP computer for the validation epoch."""
        self.map_computer = MeanAveragePrecision()

    @torch.no_grad()
    def validation_step(
        self, inputs: list[Tensor], classes: list[Tensor], boxes: list[Tensor]
    ) -> tuple[Tensor, dict[str, Any]]:
        """Perform single validation step.

        Args:
            inputs (list[Tensor]): Input features by level
            classes (list[Tensor]): Ground truth classes by sample in mini-batch
            bboxes (list[Tensor]): Ground truth boxes by sample in mini-batch

        Returns:
            tuple[Tensor, dict[str, Any]]: Total and partial or auxiliary losses
        """
        num_instances, scores, pred_classes, pred_boxes = self.forward(inputs)
        self.map_computer.update(
            [
                {"scores": s, "labels": c, "boxes": b}
                for n, s, c, b in zip(num_instances, scores, pred_classes, pred_boxes)
            ],
            [{"labels": c, "boxes": b} for c, b in zip(classes, boxes)],
        )
        return self.training_step(inputs, classes, boxes)

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
        self, inputs: list[Tensor], classes: list[Tensor], boxes: list[Tensor]
    ) -> list[Tensor]:
        num_instances, scores, pred_classes, pred_boxes = self.forward(inputs)
        visualizations: list[Tensor] = []
        with as_file(files(__package__).parent / "NotoSansMono-Bold.ttf") as font:
            for batch, image in enumerate(inputs[0]):
                image = draw_bounding_boxes(
                    (image * 255).to(torch.uint8),
                    boxes[batch],
                    [self.class_names[_] for _ in classes[batch]],
                    colors="yellow",
                    width=max(2, image.shape[1] // 100),
                    font=str(font),
                    font_size=max(10, image.shape[1] // 20),
                )
                visualizations.append(
                    draw_bounding_boxes(
                        image,
                        pred_boxes[batch][: num_instances[batch]],
                        [
                            self.class_names[_]
                            for _ in pred_classes[batch][: num_instances[batch]]
                        ],
                        colors="blue",
                        width=max(2, image.shape[1] // 100),
                        font=str(font),
                        font_size=max(10, image.shape[1] // 20),
                    )
                )
        return visualizations
