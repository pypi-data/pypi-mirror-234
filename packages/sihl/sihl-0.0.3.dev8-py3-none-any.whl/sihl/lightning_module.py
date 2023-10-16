from __future__ import annotations

import logging
from typing import Any

import lightning.pytorch as pl
import torch
from torch import Tensor
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler

from sihl.sihl_model import SihlModel


class LightningModule(pl.LightningModule):  # type:ignore
    """Lightning module wrapper for conveniently training Sihl models."""

    def __init__(
        self,
        model: SihlModel,
        optimizer: type[Optimizer] = torch.optim.Adam,
        optimizer_kwargs: dict[str, Any] | None = None,
        scheduler: type[_LRScheduler] | None = None,
        scheduler_kwargs: dict[str, Any] | None = None,
    ):
        super().__init__()
        self.model = model
        self.optimizer = optimizer
        self.optimizer_kwargs = optimizer_kwargs or {}
        self.scheduler = scheduler
        self.scheduler_kwargs = scheduler_kwargs or {}

    def forward(self, x: Tensor) -> list[Tensor | tuple[Tensor, ...]]:
        return self.model(x)  # type:ignore

    def training_step(
        self, batch: tuple[Tensor, Any], batch_idx: int
    ) -> Tensor:
        x, targets = batch
        if not isinstance(targets, list):
            targets = [targets]  # single-headed
        head_inputs = self.model.backbone(x)
        if self.model.neck:
            head_inputs = self.model.neck(head_inputs)
        losses = []
        log_options = {"on_epoch": False, "on_step": True, "prog_bar": True}
        for head_idx, (head, target) in enumerate(zip(self.model.heads, targets)):
            if isinstance(target, dict):
                loss, metrics = head.training_step(head_inputs, **target)
            else:
                loss, metrics = head.training_step(head_inputs, target)
            metrics = {f"{head_idx}/{k}": v for k, v in metrics.items()}
            try:
                self.log(f"{head_idx}/train/loss", loss, **log_options)  # type: ignore
                self.log_dict(metrics, **log_options)  # type: ignore
            except:
                pass
            losses.append(loss)
        loss = sum(losses, torch.zeros(1, device=losses[0].device))
        scheduler = self.lr_schedulers()
        if isinstance(scheduler, _LRScheduler):
            scheduler.step()
            lr = scheduler.get_last_lr()[0]
            try:
                self.log("lr", lr, **log_options)  # type: ignore
            except:
                pass
        return loss  # type:ignore

    def validation_step(
        self, batch: tuple[Tensor, Any], batch_idx: int
    ) -> Tensor:
        x, targets = batch
        if not isinstance(targets, list):
            targets = [targets]  # single-headed
        head_inputs = self.model.backbone(x)
        if self.model.neck:
            head_inputs = self.model.neck(head_inputs)
        if batch_idx == 0 and self.logger and hasattr(self.logger, "experiment"):
            for head_idx, (head, target) in enumerate(zip(self.model.heads, targets)):
                try:
                    if isinstance(target, dict):
                        images = head.visualize(head_inputs, **target)  # type: ignore
                    else:
                        images = head.visualize(head_inputs, target)
                    for sample_idx, image in enumerate(images):
                        self.logger.experiment.add_image(
                            f"{head_idx}/eval/{sample_idx}",
                            image,
                            global_step=self.global_step,
                        )
                except Exception as e:
                    logging.warn(e)
        losses = []
        for head_idx, (head, target) in enumerate(zip(self.model.heads, targets)):
            if isinstance(target, dict):
                loss, metrics = head.validation_step(head_inputs, **target)
            else:
                loss, metrics = head.validation_step(head_inputs, target)
            losses.append(loss)
        loss = sum(losses, torch.zeros(1, device=losses[0].device))
        return loss  # type:ignore

    def configure_optimizers(
        self,
    ) -> Optimizer | tuple[list[Optimizer], list[_LRScheduler]]:
        optimizer = self.optimizer(self.parameters(), **self.optimizer_kwargs)
        if self.scheduler:
            scheduler = self.scheduler(optimizer, **self.scheduler_kwargs)
            return [optimizer], [scheduler]
        return optimizer

    def on_validation_start(self) -> None:
        for head in self.model.heads:
            try:
                head.on_validation_start()
            except Exception as e:
                logging.warn(e)
                pass

    def on_validation_epoch_end(self) -> None:
        for head_idx, head in enumerate(self.model.heads):
            try:
                val_metrics = head.on_validation_end()
                val_metrics = {f"{head_idx}/{k}": v for k, v in val_metrics.items()}
                try:
                    self.log_dict(
                        val_metrics, on_epoch=True, on_step=False, prog_bar=True
                    )
                except:
                    pass
            except Exception as e:
                logging.warn(e)
                pass
