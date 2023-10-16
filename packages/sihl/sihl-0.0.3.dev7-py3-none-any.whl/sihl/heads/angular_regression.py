# TODO: make this multi-output

from __future__ import annotations  # noqa: D100

import torch
import torchmetrics
from torch import Tensor
from torch import nn


class Normalize(nn.Module):
    def forward(self, x: Tensor) -> Tensor:
        return x / torch.linalg.vector_norm(x, dim=1, keepdim=True)  # type: ignore


class AngleRegression(nn.Module):  # noqa: D101
    def __init__(self, in_channels: int) -> None:  # noqa: D107
        super().__init__()
        self.net = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(in_channels, 2),
            Normalize(),
        )

    def forward(self, inputs: list[Tensor]) -> Tensor:  # noqa: D102
        cos, sin = self.net(inputs[-1]).unbind(1)
        pred_angles = torch.atan2(sin, cos)
        return pred_angles

    def training_step(  # noqa: D102
        self, inputs: list[Tensor], angles: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        cos_sin = self.net(inputs[-1])
        targets = torch.stack([torch.cos(angles), torch.sin(angles)], dim=1)
        loss = (1 - torch.cosine_similarity(cos_sin, targets)).mean()
        return loss, {}

    def on_validation_start(self) -> None:  # noqa: D102
        self.similarity_computer = torchmetrics.CosineSimilarity(reduction="mean")

    def validation_step(  # noqa: D102
        self, inputs: list[Tensor], angles: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        cos_sin = self.net(inputs[-1])
        targets = torch.stack([torch.cos(angles), torch.sin(angles)], dim=1)
        loss = (1 - torch.cosine_similarity(cos_sin, targets)).mean()
        self.similarity_computer.update(cos_sin, targets)
        return loss, {}

    def on_validation_end(self) -> dict[str, float]:  # noqa: D102
        return {"cosine similarity": self.similarity_computer.compute().item()}
