from __future__ import annotations


try:
    from importlib_resources import as_file, files
except ImportError:
    from importlib.resources import files, as_file  # type: ignore

import torch
from torch import Tensor, nn
from torchmetrics.regression import MeanAbsoluteError, MeanSquaredError
from torchmetrics.functional import log_cosh_error
from torchvision.utils import draw_bounding_boxes


class Regression(nn.Module):
    def __init__(
        self, in_channels: list[int], num_targets: int, level: int = -1
    ) -> None:
        super().__init__()
        self.level = level
        self.net = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(in_channels[self.level], num_targets),
        )
        self.output_shapes = {"targets": ("batch_size", "num_targets")}

    def forward(self, inputs: list[Tensor]) -> Tensor:
        return self.net(inputs[self.level])  # type: ignore

    def training_step(
        self, inputs: list[Tensor], targets: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        pred_values = self.forward(inputs)
        return log_cosh_error(pred_values, targets), {}

    def on_validation_start(self) -> None:
        self.mae_computer = MeanAbsoluteError()
        self.mse_computer = MeanSquaredError()

    def validation_step(
        self, inputs: list[Tensor], targets: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        pred_values = self.net(inputs[self.level])
        loss = log_cosh_error(pred_values, targets)
        self.mae_computer.to(pred_values.device).update(pred_values, targets)
        self.mse_computer.to(pred_values.device).update(pred_values, targets)
        return loss, {}

    def on_validation_end(self) -> dict[str, float]:
        return {
            "mean absolute error": self.mae_computer.compute().item(),
            "mean squared error": self.mse_computer.compute().item(),
        }

    def visualize(self, inputs: list[Tensor], labels: Tensor) -> list[Tensor]:
        pred_values = self.forward(inputs)
        visualizations: list[Tensor] = []
        with as_file(files(__package__).parent / "NotoSansMono-Bold.ttf") as font:
            for batch, image in enumerate(inputs[0]):
                font_size = max(10, image.shape[1] // 10)
                offset = 0
                img = (image * 255).to(torch.uint8)
                for pred, target in zip(pred_values[batch], labels[batch]):
                    sign = "+" if pred >= target else "-"
                    img = draw_bounding_boxes(
                        img,
                        torch.tensor([[0, offset, 0, offset]]),
                        [f"{pred} ({target} {sign}{(target-pred).abs().item()})"],
                        colors="red",
                        width=0,
                        font=str(font),
                        font_size=font_size,
                    )
                    offset += font_size
                visualizations.append(img)
        return visualizations
