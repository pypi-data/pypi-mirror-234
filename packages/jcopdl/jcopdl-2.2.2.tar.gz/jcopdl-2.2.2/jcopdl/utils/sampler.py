import numpy as np
from torch.utils.data.sampler import WeightedRandomSampler


class BalancedRandomSampler(WeightedRandomSampler):
    """
    Automatically compute balanced weight for PyTorch WeightedRandomSampler.
    The 'balanced' heuristic is explained ini
    King, G. & Zeng, L. 2001. Logistic Regression in Rare Events Data
    https://dash.harvard.edu/bitstream/handle/1/4125045/relogit?sequence=2


    == Arguments ==
    y: np.array
        label encoded data

    replacement: bool
        If ``True``, samples are drawn with replacement.
        If not, they are drawn without replacement, which means that when a sample index
        is drawn for a row, it cannot be drawn again for that row.
    """
    def __init__(self, y, replacement: bool = True):
        n_classes = len(set(y))
        recip_freq = len(y) / (n_classes * np.bincount(y).astype(np.float64))
        weights = recip_freq[y]
        super().__init__(weights, num_samples=len(weights), replacement=replacement)
