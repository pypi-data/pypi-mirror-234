from __future__ import annotations


try:
    from importlib_resources import as_file, files
except ImportError:
    from importlib.resources import files, as_file  # type: ignore

import torch
from torch import Tensor, nn
from torchmetrics.classification import (
    MultilabelAccuracy,
    MultilabelPrecision,
    MultilabelRecall,
)
from torchvision.utils import draw_bounding_boxes


class MultilabelClassification(nn.Module):
    def __init__(
        self,
        in_channels: list[int],
        num_classes: int,
        level: int = -1,
        class_names: tuple[str, ...] | None = None,
        label_weights: list[float] | None = None,
    ) -> None:
        super().__init__()
        self.num_classes = num_classes
        self.level = level
        self.class_names = class_names or tuple(str(_) for _ in range(num_classes))
        assert len(self.class_names) == self.num_classes
        self.label_weights = torch.tensor(label_weights) if label_weights else None
        self.net = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(in_channels[self.level], num_classes),
        )
        self.output_shapes = {
            "scores": ("batch_size", num_classes),
            "classes": ("batch_size", num_classes),
        }

    def forward(self, inputs: list[Tensor]) -> tuple[Tensor, Tensor]:
        scores, classes = torch.sort(
            torch.sigmoid(self.net(inputs[self.level])), descending=True
        )
        return scores, classes

    def training_step(
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        logits = self.net(inputs[self.level])
        loss = torch.nn.functional.binary_cross_entropy_with_logits(
            logits,
            labels.to(logits.device).to(logits.dtype),
            pos_weight=self.label_weights,
        )
        return loss, {}

    def on_validation_start(self) -> None:
        self.accuracy_computer = MultilabelAccuracy(self.num_classes, average="micro")
        self.precision_computer = MultilabelPrecision(self.num_classes, average="micro")
        self.recall_computer = MultilabelRecall(self.num_classes, average="micro")

    def validation_step(
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        input = inputs[self.level]
        logits = self.net(input)
        labels = labels.to(logits.device).to(logits.dtype)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(
            logits, labels, pos_weight=self.label_weights
        )
        logits = logits.detach().float()
        labels = labels.float()
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
                font_size = max(10, image.shape[1] // 10)
                predictions = sorted(
                    self.class_names[class_idx]
                    for score, class_idx in zip(scores[batch], classes[batch])
                    if score > 0.5
                )
                targets = sorted(
                    self.class_names[class_idx]
                    for class_idx, is_true in enumerate(labels[batch])
                    if is_true
                )
                offset = 0
                img = (image * 255).to(torch.uint8)
                for target in targets:
                    img = draw_bounding_boxes(
                        img,
                        torch.tensor([[0, offset, 0, offset]]),
                        [target],
                        colors="green" if target in predictions else "yellow",
                        width=0,
                        font=str(font),
                        font_size=font_size,
                    )
                    offset += font_size
                for pred in predictions:
                    if pred in targets:
                        continue
                    img = draw_bounding_boxes(
                        img,
                        torch.tensor([[0, offset, 0, offset]]),
                        [pred],
                        colors="red",
                        width=0,
                        font=str(font),
                        font_size=font_size,
                    )
                    offset += font_size
                visualizations.append(img)
        return visualizations
