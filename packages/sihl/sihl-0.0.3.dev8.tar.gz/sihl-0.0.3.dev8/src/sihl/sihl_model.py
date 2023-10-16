from __future__ import annotations

from torch import Tensor, nn


class SihlModel(nn.Module):
    def __init__(
        self, backbone: nn.Module, neck: nn.Module | None, heads: list[nn.Module]
    ):
        super().__init__()
        self.backbone = backbone
        self.neck = neck
        self.heads = nn.ModuleList(heads)

    def forward(self, input: Tensor) -> list[Tensor | tuple[Tensor, ...]]:
        x = self.backbone(input)
        if self.neck is not None:
            x = self.neck(x)
        return [head(x) for head in self.heads]
