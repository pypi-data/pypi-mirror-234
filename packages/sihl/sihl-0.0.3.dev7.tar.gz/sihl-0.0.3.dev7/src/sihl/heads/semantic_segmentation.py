from __future__ import annotations  # noqa: D100

import torch
from torchmetrics.classification import MulticlassJaccardIndex
from torch import nn
from torch import Tensor
from torch.nn import functional
from functools import partial

from sihl.layers import ConvNormRelu
from sihl.layers import BilinearUpscaler


class SimplePyramidPoolingModule(nn.Module):
    """c.f. [PP-liteseg](https://arxiv.org/abs/2204.02681) ."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        pool_sizes: tuple[int, ...] = (1, 2, 4),
    ) -> None:  # noqa:D107
        super().__init__()
        self.pools = nn.ModuleList(
            nn.Sequential(
                nn.AvgPool2d(kernel_size=pool_size),
                ConvNormRelu(in_channels, out_channels, kernel_size=1),
            )
            for pool_size in pool_sizes
        )
        self.out_conv = ConvNormRelu(out_channels, out_channels)

    def forward(self, x: Tensor) -> Tensor:  # noqa:D102
        pooled_features = []
        for pool in self.pools:
            pooled_features.append(
                functional.interpolate(pool(x), size=x.shape[2:], mode="bilinear")
            )
        return self.out_conv(  # type:ignore
            torch.stack(pooled_features, dim=0).sum(dim=0)
        )


class SpatialUnifiedAttentionFusionModule(nn.Module):
    """c.f. [PP-liteseg](https://arxiv.org/abs/2204.02681) ."""

    def __init__(self, in_channels: int, out_channels: int) -> None:  # noqa:D107
        super().__init__()
        self.conv = nn.Sequential(
            ConvNormRelu(4, 2), ConvNormRelu(2, 1, skip_relu=True)
        )
        self.out_conv = ConvNormRelu(in_channels, out_channels)

    def forward(self, x1: Tensor, x2: Tensor) -> Tensor:  # noqa:D102
        avg_out1 = torch.mean(x1, dim=1, keepdim=True)
        max_out1, _ = torch.max(x1, dim=1, keepdim=True)
        avg_out2 = torch.mean(x2, dim=1, keepdim=True)
        max_out2, _ = torch.max(x2, dim=1, keepdim=True)
        alpha = torch.sigmoid(
            self.conv(torch.cat([avg_out1, max_out1, avg_out2, max_out2], dim=1))
        )
        return self.out_conv(x1 * alpha + x2 * (1 - alpha))  # type:ignore


class SemanticSegmentation(nn.Module):  # noqa: D101
    """c.f. [PP-liteseg](https://arxiv.org/abs/2204.02681) ."""

    def __init__(  # noqa: D107
        self,
        in_channels: list[int],
        num_classes: int,
        background_idx: int | None = None,
        level: int = -1,
        decoder_channels: tuple[int, ...] = (64, 96, 128),
        label_weights: list[float] | None = None,
        label_smoothing: float = 0.0,
    ) -> None:
        super().__init__()
        self.level = level
        self.num_classes = num_classes
        self.ignore_idx = background_idx
        self.label_weights = torch.tensor(label_weights) if label_weights else None
        self.label_smoothing = label_smoothing
        self.aggregation = SimplePyramidPoolingModule(
            in_channels=in_channels[self.level], out_channels=decoder_channels[-1]
        )
        self.upscales = nn.ModuleList([BilinearUpscaler() for _ in decoder_channels])
        self.fusions = nn.ModuleList(
            [
                SpatialUnifiedAttentionFusionModule(
                    decoder_channels[-decoder_idx - 1],
                    decoder_channels[-decoder_idx - 2],
                )
                for decoder_idx in range(len(decoder_channels) - 1)
            ]
        )
        self.out_conv = ConvNormRelu(decoder_channels[0], self.num_classes)
        self.loss = partial(
            functional.cross_entropy,
            weight=self.label_weights,
            ignore_index=self.ignore_idx or -100,
            label_smoothing=self.label_smoothing,
        )

    def raw_forward(self, inputs: list[Tensor]) -> Tensor:  # noqa:D102
        x = self.aggregation(inputs[self.level])
        for idx, (up, fuse) in enumerate(zip(self.upscales, self.fusions)):  # noqa:B905
            x = fuse(up(x), inputs[len(inputs) - 1 - idx])
        return self.out_conv(x)  # type:ignore

    def forward(self, inputs: list[Tensor]) -> Tensor:  # noqa: D102
        return torch.argmax(
            functional.interpolate(
                self.raw_forward(inputs), size=inputs[0].shape[-2:], mode="bilinear"
            ),
            dim=1,
        )

    def training_step(  # noqa: D102
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        prediction = functional.interpolate(
            self.raw_forward(inputs), size=labels.shape[-2:], mode="bilinear"
        )
        loss = self.loss(prediction, labels)
        return loss, {}

    def on_validation_start(self) -> None:  # noqa: D102
        self.mean_iou_computer = MulticlassJaccardIndex(num_classes=self.num_classes)

    def validation_step(  # noqa: D102
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        prediction = functional.interpolate(
            self.raw_forward(inputs), size=labels.shape[-2:], mode="bilinear"
        )
        loss = self.loss(prediction, labels)
        self.mean_iou_computer.update(prediction, labels)
        return loss, {}

    def on_validation_end(self) -> dict[str, float]:  # noqa: D102
        return {"mean IOU": self.mean_iou_computer.compute().item()}
