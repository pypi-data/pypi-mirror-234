from __future__ import annotations


try:
    from importlib_resources import as_file, files
except ImportError:
    from importlib.resources import files, as_file  # type: ignore

import torch
import torchmetrics
from torch import Tensor, nn
from torchvision.utils import draw_bounding_boxes


class BinaryClassification(nn.Module):
    def __init__(
        self, in_channels: list[int], level: int = -1, question: str = "positive?"
    ) -> None:
        super().__init__()
        self.level = level
        self.net = nn.Sequential(
            nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(in_channels[self.level], 1)
        )
        self.question = question
        self.output_shapes = {"scores": ("batch_size",), "classes": ("batch_size",)}

    def forward(self, inputs: list[Tensor]) -> tuple[Tensor, Tensor]:
        scores = torch.sigmoid(self.net(inputs[self.level])).squeeze(-1)
        return scores, scores > 0.5

    def training_step(
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        logits = self.net(inputs[self.level]).squeeze(-1)
        labels = labels.to(logits.dtype).to(logits.device)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        return loss, {}

    def on_validation_start(self) -> None:
        self.accuracy_computer = torchmetrics.classification.BinaryAccuracy()
        self.precision_computer = torchmetrics.classification.BinaryPrecision()
        self.recall_computer = torchmetrics.classification.BinaryRecall()

    def validation_step(
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        logits = self.net(inputs[self.level]).squeeze(-1)
        labels = labels.to(logits.dtype).to(logits.device)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        logits = logits.detach().float()
        labels = labels.detach()
        self.accuracy_computer.to(logits.device).update(logits, labels)
        self.precision_computer.to(logits.device).update(logits, labels)
        self.recall_computer.to(logits.device).update(logits, labels)
        return loss, {}

    def on_validation_end(self) -> dict[str, float]:
        return {
            "accuracy": self.accuracy_computer.compute().item(),
            "precision": self.precision_computer.compute().item(),
            "recall": self.recall_computer.compute().item(),
        }

    def visualize(self, inputs: list[Tensor], labels: Tensor) -> list[Tensor]:
        scores, classes = self.forward(inputs)
        visualizations: list[Tensor] = []
        with as_file(files(__package__).parent / "NotoSansMono-Bold.ttf") as font:
            for batch, image in enumerate(inputs[0]):
                visualizations.append(
                    draw_bounding_boxes(
                        (image * 255).to(torch.uint8),
                        torch.zeros((1, 4)),
                        [self.question + "\n" + ("Yes" if classes[batch] else "No")],
                        colors="green" if classes[batch] == labels[batch] else "red",
                        width=0,
                        font=str(font),
                        font_size=max(10, image.shape[1] // 10),
                    )
                )
        return visualizations
