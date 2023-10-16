# TODO: https://arxiv.org/pdf/2301.06122.pdf


from __future__ import annotations


try:
    from importlib_resources import as_file, files
except ImportError:
    from importlib.resources import files, as_file  # type: ignore

import torch
from torch import Tensor, nn
from torchmetrics.classification import (
    MulticlassAccuracy,
    MulticlassPrecision,
    MulticlassRecall,
)
from torchmetrics.regression import MeanAbsoluteError
from torchvision.utils import draw_bounding_boxes


def soft_labels(label: int, num_labels: int) -> Tensor:
    return torch.softmax(
        -(torch.arange(num_labels, dtype=torch.float32) - label).abs(), 0
    )


class OrdinalRegression(nn.Module):  # noqa: D101
    """https://openaccess.thecvf.com/content_CVPR_2019/papers/Diaz_Soft_Labels_for_Ordinal_Regression_CVPR_2019_paper.pdf"""

    def __init__(
        self,
        in_channels: list[int],
        num_classes: int,
        level: int = -1,
        class_names: tuple[str, ...] | None = None,
    ) -> None:
        super().__init__()
        self.num_classes = num_classes
        self.level = level
        self.class_names = class_names or tuple(str(_) for _ in range(num_classes))
        assert len(self.class_names) == self.num_classes
        self.net = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(in_channels[self.level], num_classes),
        )
        self.output_shapes = {"scores": ("batch_size",), "classes": ("batch_size",)}

    def forward(self, inputs: list[Tensor]) -> tuple[Tensor, Tensor]:
        scores, classes = torch.max(
            torch.nn.functional.softmax(self.net(inputs[self.level]), dim=1), dim=1
        )
        return scores, classes

    def training_step(
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        logits = self.net(inputs[self.level])
        targets = torch.stack([soft_labels(_.item(), self.num_classes) for _ in labels])
        loss = torch.nn.functional.cross_entropy(logits, targets.to(logits.device))
        return loss, {}

    def on_validation_start(self) -> None:
        self.accuracy_computer = MulticlassAccuracy(self.num_classes, average="micro")
        self.precision_computer = MulticlassPrecision(self.num_classes, average="micro")
        self.recall_computer = MulticlassRecall(self.num_classes, average="micro")
        self.mae_computer = MeanAbsoluteError()

    def validation_step(
        self, inputs: list[Tensor], labels: Tensor
    ) -> tuple[Tensor, dict[str, float]]:
        logits = self.net(inputs[self.level])
        labels = labels.to(logits.device)
        targets = torch.stack([soft_labels(_.item(), self.num_classes) for _ in labels])
        loss = torch.nn.functional.cross_entropy(logits, targets.to(logits.device))
        classes = torch.argmax(logits.detach(), dim=1)
        self.accuracy_computer.to(logits.device).update(classes, labels)
        self.precision_computer.to(logits.device).update(classes, labels)
        self.recall_computer.to(logits.device).update(classes, labels)
        self.mae_computer.to(logits.device).update(classes, labels)
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
                        [self.class_names[classes[batch]]],
                        colors="green" if classes[batch] == labels[batch] else "red",
                        width=0,
                        font=str(font),
                        font_size=max(10, image.shape[1] // 10),
                    )
                )
        return visualizations
