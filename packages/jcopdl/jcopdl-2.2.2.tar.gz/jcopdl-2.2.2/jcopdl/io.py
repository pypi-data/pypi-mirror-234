import torch


def load_from_checkpoint(checkpoint_path):
    ckpt = torch.load(checkpoint_path)
    ckpt.epoch += 1
    return ckpt
