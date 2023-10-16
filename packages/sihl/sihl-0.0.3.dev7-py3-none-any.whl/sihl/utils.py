from __future__ import annotations

import sys
import typing
from typing import Any

import torch
from torch import Tensor
from torch import nn


def soft_dice_loss(
    logits: Tensor, labels: Tensor, p: float = 2.0, eps: float = 1e-7
) -> Tensor:
    """https://github.com/CoinCheung/pytorch-loss/blob/master/soft_dice_loss.py
    inputs:
        logits: tensor of shape (N, H, W, ...)
        label: tensor of shape(N, H, W, ...)
    output:
        loss: tensor of shape(1, )
    """
    probs = torch.sigmoid(logits)
    numerator = 2.0 * (probs * labels).sum()
    denominator = (probs.pow(p) + labels.pow(p)).sum() + eps
    return 1.0 - numerator / denominator  # type: ignore


@typing.no_type_check
def get_func_locals_and_return(func, *args, **kwargs) -> tuple[list[Any], Any]:
    """Calls `func` with the specified args and kwargs and snatches its locals.

    Refs:
        1. https://stackoverflow.com/a/52358426
    """
    frame = None

    def snatch_locals(_frame, name, arg):
        nonlocal frame
        if name == "call":
            frame = _frame
            sys.settrace(sys._getframe(0).f_trace)
        return sys._getframe(0).f_trace

    sys.settrace(snatch_locals)

    try:
        result = func(*args, **kwargs)
    finally:
        sys.settrace(sys._getframe(0).f_trace)

    return frame.f_locals, result


@torch.no_grad()
def get_coordinate_grid(height: int, width: int, y_max: float, x_max: float) -> Tensor:
    """Generate a 2D coordinate grid tensor of given dimensions and bounds."""
    return torch.stack(
        torch.meshgrid(
            torch.linspace(y_max / height / 2, y_max - y_max / height / 2, height),
            torch.linspace(x_max / width / 2, x_max - x_max / width / 2, width),
            indexing="ij",  # NOTE: should be "xy" but that's not onnx exportable
        )[::-1]
    )


@torch.no_grad()
def get_relative_coordinate_grid(height: int, width: int, x: float, y: float) -> Tensor:
    return torch.stack(
        torch.meshgrid(
            torch.linspace(-y / (height / 2), (height - y) / (height / 2), height),
            torch.linspace(-x / (width / 2), (width - x) / (width / 2), width),
            indexing="ij",  # NOTE: should be "xy" but that's not onnx exportable
        )[::-1]
    )


def init_weights(module: nn.Module) -> None:
    """General-purpose module weights initializer."""
    if isinstance(module, (nn.Linear, nn.Embedding, nn.Conv2d)):
        nn.init.normal_(module.weight, mean=0, std=0.01)
    elif isinstance(module, (nn.BatchNorm2d, nn.GroupNorm, nn.LayerNorm)):
        nn.init.ones_(module.weight)
    if getattr(module, "bias", None) is not None:
        nn.init.zeros_(module.bias)  # type: ignore
