from __future__ import annotations

from torch import nn
from typing import Type, Protocol, Literal


class ConvNormRelu(nn.Sequential):
    """Simple Conv-Norm-Relu block."""

    def __init__(  # noqa: D107
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int = 3,
        stride: int = 1,
        padding: int = 1,
        norm: Literal["batch"] | Literal["group"] | None = "batch",
        skip_relu: bool = False,
    ):
        super().__init__(
            nn.Conv2d(
                in_channels, out_channels, kernel_size, stride, padding, bias=False
            ),
            {
                "batch": nn.BatchNorm2d(out_channels),
                "group": nn.GroupNorm(32, out_channels),
                None: nn.Identity(),
            }[norm],
            nn.Identity() if skip_relu else nn.ReLU(inplace=True),
        )


class HasInOutChannels(Protocol):
    def __init__(self, in_channels: int, out_channels: int, *args, **kwargs):  # type: ignore
        ...


class SequentialConvBlocks(nn.Sequential):
    def __init__(  # type: ignore
        self,
        in_channels: int,
        out_channels: int,
        num_layers: int,
        ConvBlock: Type[HasInOutChannels] = ConvNormRelu,
        **kwargs,
    ):
        assert num_layers > 0
        super().__init__(  # type: ignore
            ConvBlock(in_channels, out_channels, **kwargs),
            *[
                ConvBlock(out_channels, out_channels, **kwargs)
                for _ in range(num_layers - 1)
            ],
        )
