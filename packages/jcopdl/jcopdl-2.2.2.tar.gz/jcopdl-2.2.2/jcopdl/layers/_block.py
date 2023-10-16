from torch import nn

from jcopdl.layers._base import BaseBlock


class LinearBlock(BaseBlock):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, None}
    """
    def __init__(self, n_input, n_output, activation="relu", batchnorm=False, dropout=0):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("linear", nn.Linear(n_input, n_output))

        if batchnorm:
            self.append_batchnorm(n_output)

        self.append_activation(activation)

        if dropout > 0:
            self.append_dropout(dropout)

    def forward(self, x):
        return self.block(x)


class ConvBlock(BaseBlock):
    """
    available activation {relu, lrelu, sigmoid, tanh, elu, selu, lsoftmax, None}
    available pool_type {maxpool, avgpool, None}
    """
    def __init__(self, in_channel, out_channel, kernel=3, stride=1, pad=1, bias=True, activation="relu",
                 batchnorm=False, dropout=0, pool=None, pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("conv2d", nn.Conv2d(in_channel, out_channel, kernel, stride, pad, bias=bias))

        if batchnorm:
            self.append_batchnorm2d(out_channel)

        self.append_activation(activation)

        if dropout > 0:
            self.append_dropout2d(dropout)

        self.append_pooling2d(pool, pool_kernel, pool_stride)

    def forward(self, x):
        return self.block(x)


class TConvBlock(BaseBlock):
    def __init__(self, in_channel, out_channel, kernel=3, stride=1, pad=1, bias=True, activation="relu",
                 batchnorm=False, dropout=0, pool=None, pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("tconv2d", nn.ConvTranspose2d(in_channel, out_channel, kernel, stride, pad, bias=bias))

        if batchnorm:
            self.append_batchnorm2d(out_channel)

        self.append_activation(activation)

        if dropout > 0:
            self.append_dropout2d(dropout)

        self.append_pooling2d(pool, pool_kernel, pool_stride)

    def forward(self, x):
        return self.block(x)


class VGGBlock(BaseBlock):
    def __init__(self, in_channel, out_channel, n_repeat=2, kernel=3, stride=1, pad=1, bias=True, activation="relu",
                 batchnorm=False, dropout=0, pool="maxpool", pool_kernel=2, pool_stride=2):
        super().__init__()
        self.block = nn.Sequential()
        self.block.add_module("conv_block0",
                              ConvBlock(in_channel, out_channel, kernel, stride, pad, bias, activation, batchnorm, dropout))

        for i in range(1, n_repeat):
            if i == (n_repeat - 1):
                self.block.add_module(f"conv_block{i}",
                                      ConvBlock(out_channel, out_channel, kernel, stride, pad, bias, activation, batchnorm,
                                                dropout, pool, pool_kernel, pool_stride))
            else:
                self.block.add_module(f"conv_block{i}",
                                      ConvBlock(out_channel, out_channel, kernel, stride, pad, bias, activation, batchnorm,
                                                dropout))

    def forward(self, x):
        return self.block(x)
