from __future__ import annotations

try:
    from importlib_resources import as_file, files
except ImportError:
    from importlib.resources import files, as_file  # type: ignore


from typing import Any
import math
import string
import torch

from torch import nn, Tensor
from torchmetrics import WordErrorRate
from torchvision.models.resnet import Bottleneck
from torchvision.utils import draw_bounding_boxes

from sihl.utils import init_weights


class HolisticRepresentationBlock(nn.Sequential):
    def __init__(self, in_channels: int, out_channels: int, num_layers: int = 4):
        inplanes = in_channels * Bottleneck.expansion
        downsampler = nn.Conv2d(in_channels, inplanes, kernel_size=1, stride=2)
        super().__init__(
            Bottleneck(in_channels, in_channels, stride=2, downsample=downsampler),
            *(Bottleneck(inplanes, in_channels) for _ in range(num_layers - 1)),
            nn.AdaptiveAvgPool2d(output_size=1),
            nn.Flatten(),
            nn.Linear(inplanes, out_channels),
        )


class PositionalEncoding(nn.Module):
    """https://pytorch.org/tutorials/beginner/transformer_tutorial.html"""

    def __init__(self, d_model: int, dropout: float = 0, max_len: int = 5000):
        super().__init__()
        position = torch.arange(max_len).unsqueeze(1) * torch.exp(
            torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model)
        )
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position)
        pe[:, 0, 1::2] = torch.cos(position)
        self.register_buffer("pe", pe)
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x (Tensor): (seq_len, batch_size, embedding_dim)
        """
        return self.dropout(x + self.pe[: x.size(0)])  # type: ignore


class TextRecognition(nn.Module):
    PAD_CHAR = ""
    START_CHAR = "«"
    END_CHAR = "»"
    SPECIAL_CHARS = [PAD_CHAR, START_CHAR, END_CHAR]

    def __init__(
        self,
        in_channels: list[int],
        level: int = 3,
        model_dims: int = 512,
        num_head: int = 8,
        max_seq_len: int = 36,
        character_set: list[str] = list(string.digits + string.ascii_letters),
        bidirectional_decoding: bool = False,
    ):
        """https://arxiv.org/abs/1904.01375."""
        super().__init__()
        self.level = level
        self.in_channels = in_channels[self.level]
        self.model_dims = model_dims
        self.max_seq_len = max_seq_len
        assert not any(
            " " in character for character in character_set
        ), "Usage of ' ' is forbidden, consider replacing it with e.g. '_'"
        self.character_set = character_set + self.SPECIAL_CHARS
        num_chars = len(self.character_set)
        pad = self.character_set.index(self.PAD_CHAR)
        self.holistic_block = HolisticRepresentationBlock(self.in_channels, model_dims)
        self.conv1x1 = nn.Conv2d(
            self.in_channels, model_dims * 2, kernel_size=1, bias=False
        )
        self.embedding = nn.Embedding(num_chars, model_dims, padding_idx=pad)
        self.add_positional_encoding = PositionalEncoding(
            model_dims, max_len=self.max_seq_len + 1
        )
        self.decoder = nn.TransformerDecoderLayer(model_dims * 2, num_head)
        self.bidirectional_decoding = bidirectional_decoding
        if self.bidirectional_decoding:
            self.reverse_decoder = nn.TransformerDecoderLayer(model_dims * 2, num_head)
        self.fc = nn.Linear(model_dims * 2, num_chars, bias=False)
        self.loss = nn.CrossEntropyLoss(reduction="none")
        self.scale = math.sqrt(self.model_dims)
        self.apply(init_weights)
        self.output_shapes = {"output_codepoints": ("batch_size", self.max_seq_len)}

    def codepoint(self, char: str) -> int:
        """https://en.wikipedia.org/wiki/Code_point"""
        return self.character_set.index(char)

    def forward(self, inputs: list[Tensor]) -> Tensor:
        backbone_features = inputs[self.level]
        batch_size, device = backbone_features.shape[0], backbone_features.device
        holistic_features = self.holistic_block(backbone_features).unsqueeze(0)
        memory = self.conv1x1(backbone_features).flatten(2, 3).permute(2, 0, 1)

        pad, end = self.codepoint(self.PAD_CHAR), self.codepoint(self.END_CHAR)
        output_codepoints = torch.full(
            (batch_size, self.max_seq_len + 2), pad, dtype=torch.int64, device=device
        )
        output_codepoints[:, 0] = self.codepoint(self.START_CHAR)

        scale = math.sqrt(self.model_dims)
        for idx in range(1, self.max_seq_len + 1):
            y = self.add_positional_encoding(
                self.embedding(output_codepoints[:, :idx]).permute(1, 0, 2) * scale
            )  # shape: (seq_length, batch_size, embedding_dim)
            y = torch.cat([holistic_features.repeat(len(y), 1, 1), y], dim=2)
            mask = nn.Transformer.generate_square_subsequent_mask(len(y), device)
            output = self.fc(self.decoder(y, memory, mask))
            predicted_codepoint = torch.argmax(output, dim=2)[-1, :]
            predicted_codepoint[output_codepoints[:, idx - 1] == end] = end
            output_codepoints[:, idx] = predicted_codepoint
            if torch.all(predicted_codepoint == end):
                break
        for batch in range(batch_size):
            end_chars = (output_codepoints[batch] == end).nonzero()
            if len(end_chars):
                length = int(end_chars[0].item())
                output_codepoints[batch, length:] = -1
        output_codepoints = output_codepoints[:, 1:]  # remove START
        return output_codepoints

    def training_step(
        self, inputs: list[Tensor], labels: list[list[str]]
    ) -> tuple[Tensor, dict[str, Any]]:
        backbone_features = inputs[self.level]
        batch_size, device = backbone_features.shape[0], backbone_features.device
        max_label_length = max(len(_) for _ in labels)
        pad = self.codepoint(self.PAD_CHAR)
        output_codepoints = torch.full(
            (batch_size, max_label_length + 1), pad, dtype=torch.int64, device=device
        )
        output_codepoints[:, 0] = self.codepoint(self.START_CHAR)
        target_codepoints = torch.full(
            (batch_size, max_label_length + 1), pad, dtype=torch.int64, device=device
        )
        for batch, label in enumerate(labels):
            for pos, char in enumerate(label):
                output_codepoints[batch, pos + 1] = self.codepoint(char)
                target_codepoints[batch, pos] = self.codepoint(char)
            target_codepoints[batch, len(label)] = self.codepoint(self.END_CHAR)
        holistic_features = self.holistic_block(backbone_features).unsqueeze(0)
        memory = self.conv1x1(backbone_features).flatten(2, 3).permute(2, 0, 1)
        y = self.embedding(output_codepoints).permute(1, 0, 2) * self.scale
        y = self.add_positional_encoding(y)
        y = torch.cat([holistic_features.repeat(len(y), 1, 1), y], dim=2)
        mask = nn.Transformer.generate_square_subsequent_mask(len(y), device)
        output = self.fc(self.decoder(y, memory, tgt_mask=mask))
        loss = self.loss(output.permute(1, 2, 0), target_codepoints)
        loss[target_codepoints == pad] = 0  # do not penalize these
        loss = loss.mean()
        if self.bidirectional_decoding:
            reverse_labels = [label[::-1] for label in labels]
            shape = (batch_size, max_label_length + 1)
            output_codepoints = torch.full(shape, pad, dtype=torch.int64, device=device)
            output_codepoints[:, 0] = self.codepoint(self.START_CHAR)
            target_codepoints = torch.full(shape, pad, dtype=torch.int64, device=device)
            for batch, label in enumerate(reverse_labels):
                for pos, char in enumerate(label):
                    output_codepoints[batch, pos + 1] = self.codepoint(char)
                    target_codepoints[batch, pos] = self.codepoint(char)
                target_codepoints[batch, len(label)] = self.codepoint(self.END_CHAR)
            y = self.embedding(output_codepoints).permute(1, 0, 2) * self.scale
            y = self.add_positional_encoding(y)
            y = torch.cat([holistic_features.repeat(len(y), 1, 1), y], dim=2)
            mask = nn.Transformer.generate_square_subsequent_mask(len(y), device)
            output = self.fc(self.reverse_decoder(y, memory, tgt_mask=mask))
            reverse_loss = self.loss(output.permute(1, 2, 0), target_codepoints)
            reverse_loss[target_codepoints == pad] = 0  # do not penalize these
            loss = (loss + reverse_loss.mean()) / 2
        return loss, {}

    @torch.no_grad()
    def on_validation_start(self) -> None:
        # not using `CharErrorRate` because in this context,
        # characters can be made up of more than a single unicode character
        # e.g. "<UNK>" could be 1 semantic character, but has 5 unicode characters
        self.character_error_rate = WordErrorRate()
        self.matches: list[bool] = []

    @torch.no_grad()
    def validation_step(
        self, inputs: list[Tensor], labels: list[list[str]]
    ) -> tuple[Tensor, dict[str, Any]]:
        output_codepoints = self.forward(inputs)
        predictions = [
            " ".join(
                self.character_set[_] for _ in output_codepoints[batch_idx] if _ != -1
            ).strip()
            for batch_idx in range(output_codepoints.shape[0])
        ]
        ground_truths = [" ".join(label).strip() for label in labels]
        self.character_error_rate.update(predictions, ground_truths)
        self.matches.extend(
            [pred == gt for pred, gt in zip(predictions, ground_truths)]
        )
        return self.training_step(inputs, labels)

    @torch.no_grad()
    def on_validation_end(self) -> dict[str, float]:
        return {
            "character_error_rate": self.character_error_rate.compute().item(),
            "accuracy": sum(self.matches) / len(self.matches),
        }

    def visualize(self, inputs: list[Tensor], labels: list[list[str]]) -> list[Tensor]:
        output_codepoints = self.forward(inputs)
        visualizations: list[Tensor] = []
        with as_file(files(__package__).parent / "NotoSansMono-Bold.ttf") as font:
            for batch_idx, (image, label, codepoints) in enumerate(
                zip(inputs[0], labels, output_codepoints)
            ):
                prediction = " ".join(
                    self.character_set[_] for _ in codepoints if _ != -1
                )
                visualizations.append(
                    draw_bounding_boxes(
                        (image * 255).to(torch.uint8),
                        torch.zeros((1, 4)),
                        [prediction],
                        colors="green" if prediction == " ".join(label) else "red",
                        width=0,
                        font=str(font),
                        font_size=max(10, image.shape[1] // 10),
                    )
                )
        return visualizations
