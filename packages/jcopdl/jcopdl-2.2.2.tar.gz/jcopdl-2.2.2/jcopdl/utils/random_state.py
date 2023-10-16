import os
import random
import torch
import numpy as np


def set_pytorch_random_state(seed=42):
    print(f"Random state: {seed}")
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True


def pytorch_state(seed, device):
    return torch.Generator(device).manual_seed(seed)
