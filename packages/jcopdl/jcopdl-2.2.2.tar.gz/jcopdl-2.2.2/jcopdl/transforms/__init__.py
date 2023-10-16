from .augment import Standardize, NormalizeImageNet, DenormalizeImageNet
from .sequence import OneHotEncode, TruncateSequence, PadSequence


class Compose:
    """
    Composes several transforms together. 

    == Arguments ==
    transform = transforms.Compose([
        transforms.PadSequence(),
        transforms.OneHotEncode(5),
        transforms.TruncateSequence(200)
    ])
    """
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, x):
        for t in self.transforms:
            x = t(x)
        return x

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string