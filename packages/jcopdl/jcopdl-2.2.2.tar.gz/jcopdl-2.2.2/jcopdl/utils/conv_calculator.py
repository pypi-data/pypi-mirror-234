def conv_output_size(input_size, kernel, stride, pad):
    return ((input_size - kernel + 2 * pad) // stride) + 1


def tconv_output_size(input_size, kernel, stride, pad):
    return (input_size - 1) * stride + kernel - 2 * pad
