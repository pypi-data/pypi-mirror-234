import torch
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
from warnings import warn

from jcopdl.utils.nb_check import IN_NOTEBOOK
from jcopdl.utils.helper import listify
from jcopdl.exception import NotLoggedError, InvalidScaleValue, InvalidSenseValue, ModelError

if IN_NOTEBOOK:
    try:
        from IPython.display import display, HTML
        import matplotlib.pyplot as plt
    except:
        warn("Failed to import ipywidgets, fallback to console behavior")
        IN_NOTEBOOK = False


class Callback:
    """
    Callback for common PyTorch Workflow:
    - Neat Checkpoint and Logs
    - Early stopping
    - Runtime Plotting
    - Runtime Log and Reporting


    == Arguments ==
    model: torch.nn.Module
        A deep learning architecture using PyTorch nn.Module

    configs: dict
        A dictionary with any configurations value to be saved such as model configs, optimizer configs, scheduler configs, and training configs.        

    optimizer: torch.optim
        An optimizer using PyTorch torch.optim

    scheduler: optim.lr_scheduler
        A scheduler using PyTorch torch.optim.lr_scheduler

    checkpoint_every: int
        Number of epoch to save a checkpoint. Checkpoint would be deleted after the training finished.

    early_stop_patience: int
        number of patience tolerance before executing early stopping

    max_epoch: int
        Limit the training to this epoch. Use None if you want to train indefinitely.

    outdir: string
        path of output directory to save the weights, configs, and logs. You may also include subpath such as `outdir/model1` or `outdir/model2`


    == Example Usage ==
    # Initialization
    callback = Callback(model, configs, optimizer, scheduler, outdir="model")

    # Add single metric plot
    callback.add_plot("test_cost", scale="semilogy")

    # Add multi-metric in single plot
    callback.add_plot(["train_cost", "test_cost"], scale="semilogy")

    # Add multi-metric in multi subplot
    callback.add_plot(["train_cost", "test_cost"], scale="semilogy")
    callback.add_plot(["train_acc", "test_acc"], scale="linear")

    # Add image log
    callback.add_image("test_image")

    # Logging
    callback.log("test_cost", value)

    # Early Stopping
    if callback.early_stopping("test_cost"):
        break
    """
    def __init__(self, model, configs=None, optimizer=None, scheduler=None, checkpoint_every=50, early_stop_patience=5, max_epoch=None, outdir="output"):
        self.outdir = Path(outdir)   
        self.outdir.mkdir(parents=True, exist_ok=True)
        
        self._check_value(model, configs, max_epoch)
        
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.configs = configs
        
        self.checkpoint_every = checkpoint_every
        self.early_stop_patience = early_stop_patience
        self.best_metric = None
        self.best_epoch = None

        self.logs = {}
        self.epoch = 1
        self.early_stop = 0
        
        self._report_nb = None

        self._graph_nb = None
        self._graph_fig = None
        self._graph_axes = None        
        self._graph_metrics = []
        self._graph_scales = []

        self._image_nb = None
        self._image_metrics = []

    def early_stopping(self, sense, monitor, load_best_when_stop=True, n_log=10, plot=True, plot_image=True, figsize="auto"):
        """
        sense: {"maximize", "minimize"}
            Sense of the metric's.
            - use "minimize" if lower is better
            - use "maximize" if higher is better

        monitor: str
            metric benchmark for early stopping        
        """
        if not IN_NOTEBOOK:
            plot = False
            plot_image = False
        
        if monitor not in self.logs:
            raise NotLoggedError(f'Metric {monitor} is not logged. Please use callback.log("{monitor}", value).')

        # Show report
        self.log("epoch", self.epoch)
        if IN_NOTEBOOK:
            report_table = HTML(pd.DataFrame(self.logs).set_index("epoch").tail(n_log).to_html())
            if self._report_nb is None:
                self._report_nb = display(report_table, display_id=True)
            else:
                self._report_nb.update(report_table)
        else:
            report = f'Epoch {self.epoch:5}\n'
            report += " | ".join([f'{k.title():10} = {v[-1]:.4f}' for k, v in self.logs.items() if k != "epoch"])
            print(report + "\n")        
            
        # Save checkpoint
        if self.epoch % self.checkpoint_every == 0:
            self._save_ckpt()
            
        # Early stopping logic
        if sense not in ["maximize", "minimize"]:
            raise InvalidSenseValue('Available sense {"maximize", "minimize"}')
        
        if self.best_metric is None:
            self.best_metric = 0 if sense == "maximize" else np.inf
            self.best_epoch = 1

        last_metric = self.logs[monitor][-1]
        is_improve = last_metric > self.best_metric if sense == "maximize" else last_metric < self.best_metric
            
        stop = False
        if is_improve:
            self.best_metric = last_metric
            self.best_epoch = self.epoch
            self.early_stop = 0
            self._save_best()
        else:
            self.early_stop += 1
            if not IN_NOTEBOOK:
                print(f"\x1b[31m==> EarlyStop patience = {self.early_stop:2} | Best {monitor}: {self.best_metric:.4f}\x1b[0m")

            if self.early_stop == self.max_epoch:
                print(f'\x1b[31m==> Max epoch reached at epoch: {self.epoch} | Best {monitor}: {self.best_metric:.4f}\x1b[0m')
                print(f'\x1b[31m==> Best model is saved at {self.outdir}\x1b[0m')
                stop = True                
            elif self.early_stop >= self.early_stop_patience:
                print(f'\x1b[31m==> Execute Early Stopping at epoch: {self.epoch} | Best {monitor}: {self.best_metric:.4f}\x1b[0m')
                print(f'\x1b[31m==> Best model is saved at {self.outdir}\x1b[0m')
                stop = True

        # Plot if there are any registered metrics
        if plot:
            with plt.style.context("seaborn-bright"):
                self._plot_metrics(monitor, figsize)

        if plot_image:
            self._plot_images()
                
        # Cleanup and load best when stop                
        if stop and load_best_when_stop:
            self.model = torch.load(self.outdir / "model_best.pth", map_location="cpu")
            if self.optimizer is not None:
                self.optimizer = torch.load(self.outdir / "optimizer_best.pth", map_location="cpu")
            if self.scheduler is not None:
                self.scheduler = torch.load(self.outdir / "scheduler_best.pth", map_location="cpu")
                
        self.epoch += 1
        return stop

    def add_plot(self, metrics, scale="linear"):
        """
        Please make sure that the registered metrics is logged.
        Available scale: {"linear", "semilogy"}
        """
        if scale not in ["linear", "semilogy"]:
            raise InvalidScaleValue('Available scale {"linear", "semilogy"}')
            
        metrics = listify(metrics)
        self._graph_metrics.append(metrics)
        self._graph_scales.append(scale)

    def add_image(self, metrics): 
        metrics = listify(metrics)
        for metric in metrics:
            log_path = self.outdir / "image_logs" / metric
            log_path.mkdir(parents=True, exist_ok=True)
        self._image_metrics.extend(metrics)
        
    def _plot_metrics(self, monitor, figsize):
        # Skip plot if no registered metrics
        if not bool(self._graph_metrics):
            return

        if figsize == "auto":
            figsize = (7*len(self._graph_metrics), 5)
        
        if self._graph_nb is None:
            self._graph_fig, axes = plt.subplots(1, len(self._graph_metrics), figsize=figsize)
            if len(self._graph_metrics) == 1:
                axes = [axes] 
            self._graph_axes = axes

            for ax, metrics, scale in zip(self._graph_axes, self._graph_metrics, self._graph_scales):
                ax.set_xlabel("Epoch")
                for metric in metrics:
                    self._plot(ax, self.logs["epoch"], self.logs[metric], scale, metric)
                ax.legend()                        
            self._graph_nb = display(self._graph_fig, display_id=True)
        else:
            for ax, metrics, scale in zip(self._graph_axes, self._graph_metrics, self._graph_scales):
                ax.clear()
                ax.set_xlabel("Epoch")  
                for metric in metrics:
                    self._plot(ax, self.logs["epoch"], self.logs[metric], scale, metric)
                    if metric == monitor:
                        self._plot(ax, self.best_epoch, self.best_metric, "scatter", "best")
                        ax.set_title(f"Patience: {self.early_stop:2} | Best {monitor}: {self.best_metric:.4f}", fontsize=12)
                ax.legend()
            self._graph_nb.update(self._graph_fig)

    def _plot_images(self):
        # Skip plot if no registered metrics
        if not bool(self._image_metrics):
            return
        
        if self._image_nb is None:
            self._image_nb = [display(Image.open(self.logs[metric][-1]), display_id=True) for metric in self._image_metrics]
        else:
            for nb, metric in zip(self._image_nb, self._image_metrics):
                nb.update(Image.open(self.logs[metric][-1]))
                
    def log(self, name, value):
        if type(value) == torch.Tensor:
            value = value.item()
        if name not in self.logs:
            self.logs[name] = []
        self.logs[name].append(value)

    def log_image(self, name, pil_image):
        if name not in self.logs:
            self.logs[name] = []
        log_path = self.outdir / "image_logs" / name / f"{self.epoch:0>5}.png"
        pil_image.save(log_path)
        self.logs[name].append(log_path)

    def reset_nb(self):
        self._report_nb = None
        self._graph_nb = None        
        self._image_nb = None
        
    def change_early_stop_patience(self, patience):
        self.early_stop_patience = patience

    def _save_best(self):
        torch.save(self.model, self.outdir / f'model_best.pth')
        if self.optimizer is not None:
            torch.save(self.optimizer, self.outdir / f'optimizer_best.pth')
        if self.scheduler is not None:
            torch.save(self.scheduler, self.outdir / f'scheduler_best.pth')
            
        try:
            pd.DataFrame(self.logs).to_csv(self.outdir / "logs.csv", index=None)
        except:
            torch.save(self.logs, self.outdir / "logs.pth")

    def _save_ckpt(self):
        ckpt_path = self.outdir / "checkpoint"
        ckpt_path.mkdir(parents=True, exist_ok=True)
        
        metadata = {
            "report_nb": self._report_nb,
            "graph_nb": self._graph_nb,
            "image_nb": self._image_nb,
            "graph_fig": self._graph_fig,
            "graph_axes": self._graph_axes
        }

        self._report_nb = None
        self._graph_nb = None
        self._image_nb = None
        self._graph_fig = None
        self._graph_axes = None
        torch.save(self, ckpt_path / f'epoch_{self.epoch:0>5}.pth')
        
        self._report_nb = metadata["report_nb"]
        self._graph_nb = metadata["graph_nb"]
        self._image_nb = metadata["image_nb"]
        self._graph_fig = metadata["graph_fig"]
        self._graph_axes = metadata["graph_axes"]
        

    def _check_value(self, model, configs, max_epoch):
        self.max_epoch = max_epoch if max_epoch is not None else np.inf
            
        if (configs is not None) and isinstance(configs, dict):
            torch.save(configs, self.outdir / "configs.pth")

        if model.__module__ == "__main__":            
            raise ModelError(f'Please write model in script (ex: model.py) and import it properly.\n>> from model import {model._get_name()}')

    @staticmethod
    def _plot(ax, x, y, scale, label):
        if scale == "linear":
            ax.plot(x, y, label=label)
        elif scale == "semilogy":
            ax.semilogy(x, y, label=label)
        elif scale == "scatter":
            ax.scatter(x, y, label=label)