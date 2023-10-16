import torch
from torch import nn
import torch.nn.functional as F
from jcopdl.layers._layers import conv_relu_block, tconv_block


class UNetEncoder(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.encoders = nn.ModuleList()
        for c_in, c_out in zip(channels[:-1], channels[1:]):
            self.encoders.append(nn.Sequential(
                conv_relu_block(c_in, c_out, batch_norm=True),
                conv_relu_block(c_out, c_out, batch_norm=True)
            ))

    def forward(self, x):
        encoded = []
        for i, encoder in enumerate(self.encoders):
            if i == 0:
                x = encoder(x)
                encoded.append(x)
            else:
                x = encoder(F.max_pool2d(x, 2, 2))
                encoded.append(x)
        return encoded
    

class UNetDecoder(nn.Module):
    def __init__(self, channels, mode="tconv"):
        super().__init__()
        assert mode in ["tconv", "bilinear"]

        self.upsamplers = nn.ModuleList()
        self.decoders = nn.ModuleList()
        
        decoder_channels = channels[:-1]
        for c_in, c_out in zip(decoder_channels[:-1], decoder_channels[1:]):
            if mode == "tconv":
                self.upsamplers.append(tconv_block(c_in, c_in))
            elif mode == "bilinear":
                self.upsamplers.append(nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True))

            self.decoders.append(nn.Sequential(
                conv_relu_block(c_in + c_out, c_out, batch_norm=True),
                conv_relu_block(c_out, c_out, batch_norm=True)
            ))
            
        self.channel_pooling = nn.Conv2d(channels[-2], channels[-1], kernel_size=1)

    def forward(self, x):
        x = x[::-1]
        x, x_encoded = x[0], x[1:]
        for upsampler, decoder, x_enc in zip(self.upsamplers, self.decoders, x_encoded):
            x = torch.cat([upsampler(x), x_enc], dim=1)
            x = decoder(x)
        x = self.channel_pooling(x)
        return x