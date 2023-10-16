import io
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

import torch
from torchvision.utils import make_grid
from torchvision.transforms.functional import to_pil_image


def visualize_image_batch(images, n_col=8):
    if isinstance(images, list):
        images = torch.stack(images, dim=0)    
    grid = make_grid(images, nrow=n_col)
    return to_pil_image(grid)


def visualize_prediction_batch(images, labels, preds, classes=None, image_scale=2, fontsize=8, bg_color="white", to_pillow=True):
    n_data = images.size(0)
    assert len(labels) == len(preds) == n_data
    preds, labels = preds.cpu(), labels.cpu()

    if classes is not None:
        classes = np.array(classes)
        preds = classes[preds]
        labels = classes[labels]

    # compute n_row, n_col and figsize
    n_col = 8
    n_row = n_data // n_col + (n_data % n_col > 0)
    figsize=(image_scale*n_col, image_scale*n_row)

    fig, axes = plt.subplots(n_row, n_col, figsize=figsize)
    fig.set_facecolor(bg_color)
    fig.subplots_adjust(wspace=0.05, hspace=0.15)
    for ax in axes.flatten():
        ax.axis('off');

    for image, label, pred, ax in zip(images, labels, preds, axes.flatten()):
        ax.imshow(image.permute(1, 2, 0).cpu())
        font = {"color": 'r', "fontsize": fontsize} if label != pred else {"color": 'g', "fontsize": fontsize}
        ax.set_title(f"{label} | P: {pred}", fontdict=font);
    fig.tight_layout()

    if to_pillow:
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png');
        plt.close()
        fig = Image.open(img_buf)
    return fig


def plot_confusion_matrix(cm, labels, figsize=(8, 8), fontsize=10, colormap="Blues"):
    acc = cm.trace() / cm.sum()
    
    fig = plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, square=True, cmap=colormap, cbar=False, xticklabels=labels, yticklabels=labels,
                fmt="d", annot_kws={"fontsize": fontsize})
    plt.title(f'Accuracy: {acc:.3f}', fontsize=fontsize+1)
    plt.xlabel('Prediction', fontsize=fontsize+1)
    plt.ylabel('Actual', fontsize=fontsize+1)
    plt.yticks(rotation=0, verticalalignment='center')
    return fig
