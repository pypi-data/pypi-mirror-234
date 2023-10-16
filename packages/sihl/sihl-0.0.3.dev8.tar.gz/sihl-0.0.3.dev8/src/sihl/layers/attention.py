from __future__ import annotations  # noqa: D100

import torch
from torch import nn, Tensor


class SpatialAttention(nn.Module):
    """c.f. https://arxiv.org/abs/1807.06521 ."""

    def __init__(self, kernel_size: int = 7) -> None:  # noqa:D107
        super().__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size, padding=kernel_size // 2)

    def forward(self, x: Tensor) -> Tensor:  # noqa:D102
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        return torch.sigmoid(self.conv(torch.cat([avg_out, max_out], dim=1)))


class ChannelAttention(nn.Module):
    """c.f. https://arxiv.org/abs/1807.06521 ."""

    def __init__(self, in_channels: int, ratio: int = 16) -> None:  # noqa:D107
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, in_channels // ratio, kernel_size=1),
            nn.ReLU(),
            nn.Conv2d(in_channels // ratio, in_channels, kernel_size=1),
        )

    def forward(self, x: Tensor) -> Tensor:  # noqa:D102
        avg_out = self.conv(self.avg_pool(x))
        max_out = self.conv(self.max_pool(x))
        return torch.sigmoid(avg_out + max_out)
