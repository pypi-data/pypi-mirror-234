from jcopdl.layers._block import LinearBlock, ConvBlock, TConvBlock


def linear_block(n_in, n_out, activation='relu', batch_norm=False, dropout=0.):
    return LinearBlock(n_in, n_out, activation, batch_norm, dropout)


def conv_block(c_in, c_out, kernel=3, stride=1, pad=1, bias=True, activation='relu', batch_norm=False, dropout=0,
               pool_type='maxpool', pool_kernel=2, pool_stride=2):
    return ConvBlock(c_in, c_out, kernel, stride, pad, bias, activation, batch_norm, dropout, pool_type, pool_kernel,
                     pool_stride)


def conv_relu_block(c_in, c_out, kernel=3, stride=1, pad=1, bias=True, activation='relu', batch_norm=False, dropout=0):
    return ConvBlock(c_in, c_out, kernel, stride, pad, bias, activation, batch_norm, dropout, pool=None)


def tconv_block(c_in, c_out, kernel=4, stride=2, pad=1, bias=True, activation='relu', batch_norm=False, dropout=0,
                pool_type=None, pool_kernel=2, pool_stride=2):
    return TConvBlock(c_in, c_out, kernel, stride, pad, bias, activation, batch_norm, dropout, pool_type, pool_kernel,
                      pool_stride)
