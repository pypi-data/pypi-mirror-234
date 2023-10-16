from torch import nn


class BaseBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.block = None

        self._activation_map = {
            "relu": nn.ReLU(),
            "lrelu": nn.LeakyReLU(),
            "sigmoid": nn.Sigmoid(),
            "tanh": nn.Tanh(),
            "elu": nn.ELU(),
            "selu": nn.SELU(),
            "silu": nn.SiLU(),
            "gelu": nn.GELU(),
            "lsoftmax": nn.LogSoftmax(dim=1),
            "softmax": nn.Softmax(dim=1),
            "identity": nn.Identity(),
            "none": nn.Identity()
        } 

    def append_activation(self, activation):
        if isinstance(activation, str):
            if activation not in self._activation_map:
                raise Exception(f"jcopdl supports these activations ({', '.join(self._activation_map.keys())})")
            self.block.add_module(activation.title(), self._activation_map[activation])
        elif activation.__module__ == "torch.nn.modules.activation":
            self.block.add_module(activation._get_name(), activation)
        elif activation is not None:
            raise Exception(f"jcopdl supports these activations ({', '.join(self._activation_map.keys())})")

    def append_dropout(self, dropout):
        self.block.add_module("do", nn.Dropout(dropout))

    def append_dropout2d(self, dropout):
        self.block.add_module("do", nn.Dropout2d(dropout))

    def append_batchnorm(self, n):
        self.block.add_module("bn", nn.BatchNorm1d(n))

    def append_batchnorm2d(self, n):
        self.block.add_module("bn", nn.BatchNorm2d(n))

    def append_pooling(self, pool, pool_kernel, pool_stride):
        if pool == "maxpool":
            self.block.add_module("maxpool", nn.MaxPool1d(pool_kernel, pool_stride))
        elif pool == "avgpool":
            self.block.add_module("avgpool", nn.AvgPool1d(pool_kernel, pool_stride))
        elif pool is not None:
            raise Exception("jcopdl supports these pooling ({maxpool, avgpool, None})")

    def append_pooling2d(self, pool, pool_kernel, pool_stride):
        if pool == "maxpool":
            self.block.add_module("maxpool", nn.MaxPool2d(pool_kernel, pool_stride))
        elif pool == "avgpool":
            self.block.add_module("avgpool", nn.AvgPool2d(pool_kernel, pool_stride))
        elif pool is not None:
            raise Exception("jcopdl supports these pooling ({maxpool, avgpool, None})")
