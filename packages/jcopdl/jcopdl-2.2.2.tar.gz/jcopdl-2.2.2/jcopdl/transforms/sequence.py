import numpy as np

import torch
from torch.nn.utils.rnn import pad_sequence

        
class OneHotEncode(torch.nn.Module):
    """OneHot Encode an integer"""

    def __init__(self, n_vocab):
        super().__init__()
        self.n_vocab = n_vocab

    def forward(self, x):
        one_hot = np.zeros((np.multiply(*x.shape), self.n_vocab), dtype=np.float32)
        one_hot[np.arange(one_hot.shape[0]), x.flatten()] = 1.
        one_hot = one_hot.reshape((*x.shape, self.n_vocab))
        one_hot = torch.FloatTensor(one_hot)
        return one_hot


class TruncateSequence(torch.nn.Module):
    """Truncate sequence data"""
    def __init__(self, n_truncate):
        super().__init__()
        self.n_truncate = n_truncate

    def forward(self, x):
        if x.dim() == 3:
            Xprior = x[:, :-self.n_truncate, :]
            Xtrunc = x[:, -self.n_truncate:, :]
        elif x.dim() == 2:
            Xprior = x[:, :-self.n_truncate]
            Xtrunc = x[:, -self.n_truncate:]
        else:
            raise Exception("Input must be in dimension 2 or 3")
        return (Xprior, Xtrunc)
        

class PadSequence(torch.nn.Module):
    """Pad sequences to the longest sequence"""
    def __init__(self, pad_id=0):
        super().__init__()
        self.pad_id = pad_id
    
    def forward(self, x):
        x = [torch.LongTensor(seq) for seq in x]
        return pad_sequence(x, batch_first=True, padding_value=self.pad_id)

