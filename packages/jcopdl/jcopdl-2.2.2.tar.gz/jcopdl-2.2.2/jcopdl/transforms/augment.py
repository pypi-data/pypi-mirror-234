import torch
import torchvision.transforms.functional as F

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


class Standardize(torch.nn.Module):
    """Standardize image using Standard Scaling."""
    def __init__(self, normalize=True):
        super().__init__()
        self.normalize = normalize

    def forward(self, x):
        bs, c = x.shape[:2]
        tmp = x.view(bs, c, -1)
        mean, std = tmp.mean(2, keepdims=True), tmp.std(2, keepdims=True)
        x = (x - mean) / (std + 1e-6)

        if self.normalize:
            x = (x + 5) / 10
            x = x.clamp_(0, 1)
        return x


class NormalizeImageNet(torch.nn.Module):
    """Normalize image with ImageNet mean and std"""
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return F.normalize(x, mean=IMAGENET_MEAN, std=IMAGENET_STD, inplace=True)


class DenormalizeImageNet(torch.nn.Module):
    """Denormalize image with ImageNet mean and std"""
    def __init__(self, clip_value=True):
        super().__init__()
        self.clip_value = clip_value

    def forward(self, x):
        x = F.normalize(x, mean=[-m / s for m, s in zip(IMAGENET_MEAN, IMAGENET_STD)], std=[1.0 / s for s in IMAGENET_STD], inplace=True)
        if self.clip_value:
            x = x.clamp_(0, 1)
        return x

