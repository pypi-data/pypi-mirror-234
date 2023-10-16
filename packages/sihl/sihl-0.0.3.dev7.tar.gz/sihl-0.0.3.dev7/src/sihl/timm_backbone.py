from __future__ import annotations

import logging
from math import log

import timm
import torch
from torch import Tensor, nn

from sihl.torchvision_backbone import Normalize, PadToMultipleOf


class TimmBackbone(nn.Module):
    def __init__(
        self,
        name: str,
        pretrained: bool = False,
        input_channels: int = 3,
        frozen_levels: int = 1,
    ):
        super().__init__()
        self.name = name
        self.dummy_input = torch.zeros((1, input_channels, 64, 64))
        try:
            model = timm.create_model(name, features_only=True)
            self.model = timm.create_model(
                self.name,
                features_only=True,
                out_indices=(0, 1, 2, 3, 4),
                scriptable=True,
                exportable=True,
                pretrained=pretrained,
                in_chans=input_channels,
            )
            assert all(log(_, 2).is_integer() for _ in model.feature_info.reduction())
            self.model(self.dummy_input)
        except (RuntimeError, AttributeError, AssertionError) as error:
            raise ValueError(f"Architecture {name} is not supported.") from error
        self.normalize = (
            Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
            if pretrained and input_channels == 3
            else Normalize(mean=(0.5,), std=(0.5,))
        )
        self.pad = PadToMultipleOf(32)
        # freeze modules in first `frozen_levels` levels
        for parameter in self.model.parameters():
            parameter.requires_grad = True
        if frozen_levels != 0:
            len_levels = len(self.model.feature_info.module_name())
            frozen_levels = (
                len_levels if frozen_levels < 0 else min(frozen_levels, len_levels)
            )
            stop_freeze = self.model.feature_info.module_name()[frozen_levels - 1]
            last_level_reached = False
            for layer_name in [_[0] for _ in self.model.named_modules()]:
                if last_level_reached:
                    break
                if layer_name == "" or "." in layer_name:
                    continue
                if stop_freeze in layer_name:
                    last_level_reached = True
                logging.info(f"freezing {layer_name}")
                for parameter in getattr(self.model, layer_name).parameters():
                    parameter.requires_grad = False
                    if isinstance(parameter, nn.BatchNorm2d):
                        parameter.track_running_stats = False
                        parameter.eval()
        self.out_channels = [input_channels] + self.model.feature_info.channels()

    def forward(self, x: Tensor) -> list[Tensor]:
        return [x] + list(self.model(self.pad(self.normalize(x))))
