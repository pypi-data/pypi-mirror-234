from functools import partial

from torch import Tensor, nn
from torch.nn.functional import interpolate

from sihl.layers.convblocks import ConvNormRelu


class StridedDownscaler(ConvNormRelu):
    def __init__(self, num_channels: int, **kwargs):  # type: ignore
        super().__init__(num_channels, num_channels, stride=2, **kwargs)


class BilinearUpscaler(nn.Module):
    def __init__(self, scale: float = 2.0, **kwargs):  # type: ignore
        super().__init__(**kwargs)
        self.interpolate = partial(interpolate, scale_factor=scale, mode="bilinear")

    def forward(self, x: Tensor) -> Tensor:
        return self.interpolate(x)  # type: ignore


# class BilinearAdditiveUpscaler(nn.Module):
