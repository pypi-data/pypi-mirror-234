from __future__ import annotations

from torch import nn, Tensor

from sihl.utils import init_weights
from sihl.layers.convblocks import ConvNormRelu
from sihl.layers.scalers import BilinearUpscaler, StridedDownscaler


class FPN(nn.Module):
    def __init__(
        self, in_channels: list[int], out_channels: int, min_level: int, max_level: int
    ) -> None:
        super().__init__()
        assert 0 < min_level < max_level
        self.in_channels = in_channels
        self.out_channels = in_channels[:min_level] + [
            out_channels for _ in range(min_level, max_level + 1)
        ]
        self.min_level = min_level
        self.max_out_level = max_level
        self.max_in_level = min(max_level, len(in_channels))

        self.top_lateral_connection = ConvNormRelu(
            in_channels[self.max_in_level - 1], out_channels, kernel_size=1, padding=0
        )
        self.lateral_connections = nn.ModuleList(
            [
                ConvNormRelu(chans, out_channels, kernel_size=1, padding=0)
                for chans in in_channels[self.min_level : self.max_in_level - 1]
            ][::-1]
        )
        self.upscalers = nn.ModuleList(
            [BilinearUpscaler() for _ in range(self.max_in_level - self.min_level - 1)]
        )
        self.downscalers = nn.ModuleList(
            [
                StridedDownscaler(out_channels) 
                for _ in range(self.max_out_level - self.max_in_level + 1)
            ]
        )
        self.output_convs = nn.ModuleList(
            [
                ConvNormRelu(out_channels, out_channels)
                for _ in range(self.max_in_level - self.min_level + 1)
            ]
        )
        self.apply(init_weights)

    def forward(self, inputs: list[Tensor]) -> list[Tensor]:
        """Forward pass

        Args:
            inputs (List[Tensor]): Shallow-to-deep input tensors

        Returns:
            List[Tensor]: Shallow-to-deep output tensors
        """
        # populate in reversed order (deep to shallow)
        outs = [self.top_lateral_connection(inputs[self.max_in_level - 1])]
        for idx, (lateral_connection, upscaler) in enumerate(
            zip(self.lateral_connections, self.upscalers)
        ):
            outs.append(
                lateral_connection(inputs[self.max_in_level - idx - 2])
                + upscaler(outs[-1])
            )
        # reset list order (shallow-to-deep) and apply output convs
        outs = [conv(out) for conv, out in zip(self.output_convs, outs[::-1])]
        for extra_layer in self.downscalers:  # apply extra downscaling layers if any
            outs.append(extra_layer(outs[-1]))
        return inputs[:self.min_level] + outs
