#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

__all__ = ["BufferTempConv", "DepthwiseBufferTempConv", "reset_buffers",
           "QuantizedBufferTempConv", "QuantizedDepthwiseBufferTempConv"]

import tensorflow as tf
from keras import layers
from .layers_base import (register_quantize_target, rescale_outputs, tensor_inputs,
                          neural_layer_init, register_aligned_inputs)
from .recorders import TensorRecorder
from ..tensors import FixedPoint


@tf.keras.utils.register_keras_serializable()
class BaseBufferTempConv(layers.Layer):
    """The base class for BufferTempConv layers.

    Args:
        kernel_size (int): an integer, specifying the height and width of the 1D convolution window.
        use_bias (bool, optional): whether the layer uses a bias vector. Defaults to False
    """

    def __init__(self, kernel_size, use_bias=False, **kwargs):
        super().__init__(**kwargs)
        self.kernel_size = kernel_size
        self.use_bias = use_bias
        self.reset_buffer()

    def _fifo_op(self, new_sample):
        """Pushes a new sample to the FIFO, popping out the oldest one.

        Args:
            new_sample (tf.Tensor): the new handled input.
        """
        if self.fifo is None:
            zeros = tf.zeros_like(new_sample)
            self.fifo = tf.tile(tf.expand_dims(zeros, axis=-2), [1, 1, 1, self.kernel_size, 1])

        # FIFO pop operation
        self.fifo = tf.gather(self.fifo, tf.range(1, self.fifo.shape[-2]), axis=-2)
        # FIFO push operation
        self.fifo = tf.concat([self.fifo, tf.expand_dims(new_sample, axis=-2)], axis=-2)

    def _align_fifo(self):
        """Helper to align the layer FIFO and expand it into a higher bitwidth.
        The input_shift is also created if doesn't exist and ready to be stored.

        Returns:
            fifo_aligned: The FixedPoint expanded and aligned fifo.
        """
        # Expand the inputs to a higher bitwidth to avoid saturation and align them.
        fifo_aligned, shift = self.fifo.expand(self.buffer_bitwidth)
        self.input_shift(shift)
        return fifo_aligned

    def call(self, inputs):
        raise NotImplementedError

    def reset_buffer(self):
        """Helper that allows reinitializing the layer internal buffer. it should be called before
        doing any inference on this layer.
        """
        self.fifo = None

    def get_config(self):
        config = super().get_config()
        config.update({
            'kernel_size': self.kernel_size,
            'use_bias': self.use_bias
        })
        return config


def _buffer_temp_conv_op(fifo, kernel):
    """ BufferTempConv layer main op function.

    Args:
        fifo (tf.Tensor): the remembered inputs stacked in the layer fifo.
        kernel (tf.Tensor): the layer kernel weights.

    Returns:
        output: the layer output tensor.
    """
    # Reshape FIFO to perform a conv2d: (B, H, W, T, C) -> (B, H, W, T * C)
    _, H, W, T, C = fifo.shape
    fifo_reshaped = tf.reshape(fifo, shape=(-1, H, W, T*C))
    # (B, H, W, T * C) * (1, 1, T * C, F) -> (B, H, W, F)
    output = tf.nn.convolution(fifo_reshaped, kernel)
    return output


def _depthwise_buffer_temp_conv_op(fifo, kernel):
    """ DepthwiseBufferTempConv layer main op function.

    Args:
        fifo (tf.Tensor): the remembered inputs stacked in the layer fifo.
        kernel (tf.Tensor): the layer kernel weights.

    Returns:
        output: the layer output tensor.
    """
    # (B, H, W, T, C) * (T, C) -> (B, H, W, T, C)
    output = tf.math.multiply(fifo, kernel)
    # (B, H, W, T, C) -> (B, H, W, C)
    output = tf.math.reduce_sum(output, axis=-2)

    return output


@tf.keras.utils.register_keras_serializable()
class BufferTempConv(BaseBufferTempConv):
    """A Conv3D layer working on the first dimension implemented as a Conv1D associated with a FIFO.
The FIFO buffer acts as a temporal sliding window on inputs for which content is convolved with the
layer kernel.

    Expects the input data to be streamed into the layer sequentially in time.

    Args:
        filters (int): the dimensionality of the output space (i.e. the number of output filters in
            the convolution).
        kernel_size (int): an integer, specifying the height and width of the 1D convolution window.
        use_bias (bool, optional): whether the layer uses a bias vector. Defaults to False
    """

    def __init__(self,
                 filters,
                 kernel_size,
                 use_bias=False,
                 **kwargs):
        super().__init__(kernel_size, use_bias, **kwargs)
        self.filters = filters

    def build(self, input_shape):
        super().build(input_shape)
        kernel_shape = (1, 1, self.kernel_size*input_shape[-1], self.filters)
        self.kernel = self.add_weight(name="kernel", shape=kernel_shape)
        if self.use_bias:
            self.bias = self.add_weight(name="bias", shape=(self.filters,))

    def call(self, inputs):
        # FIFO pop/push, shape is (B, H, W, T, C)
        self._fifo_op(inputs)
        output = _buffer_temp_conv_op(self.fifo, self.kernel)
        if self.use_bias:
            output = tf.math.add(output, self.bias)
        return output

    def get_config(self):
        config = super().get_config()
        config.update({
            'filters': self.filters
        })
        return config


@tf.keras.utils.register_keras_serializable()
class DepthwiseBufferTempConv(BaseBufferTempConv):
    """Similar to its BufferTempConv sibling, this layer operates with a depthwise kernel.

    Expects the input data to be streamed into the layer sequentially in time.

    Args:
        kernel_size (int): an integer, specifying the height and width of the 1D convolution window.
        use_bias (bool, optional): whether the layer uses a bias vector. Defaults to False
    """

    def build(self, input_shape):
        super().build(input_shape)
        kernel_shape = (self.kernel_size, input_shape[-1])
        self.kernel = self.add_weight(name="kernel", shape=kernel_shape)
        if self.use_bias:
            self.bias = self.add_weight(name="bias", shape=(input_shape[-1],))

    def call(self, inputs):
        # FIFO pop/push, shape is (B, H, W, T, C)
        self._fifo_op(inputs)

        output = _depthwise_buffer_temp_conv_op(self.fifo, self.kernel)
        if self.use_bias:
            output = tf.math.add(output, self.bias)

        return output


@register_quantize_target([BufferTempConv])
@register_aligned_inputs
@tf.keras.utils.register_keras_serializable()
class QuantizedBufferTempConv(BufferTempConv):
    """A quantized version of the BufferTempConv layer that operates on quantized inputs and
    weights.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    @neural_layer_init(False)
    def __init__(self, *args, quant_config=None, **kwargs):
        self.input_shift = TensorRecorder(name="input_shift")

    @tensor_inputs([FixedPoint, tf.Tensor])
    @rescale_outputs
    def call(self, inputs):
        # FIFO pop/push, shape is (B, H, W, T, C)
        self._fifo_op(inputs)
        # Align FIFO
        fifo_aligned = self._align_fifo()
        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel)
        outputs = _buffer_temp_conv_op(fifo_aligned, kernel)
        if self.use_bias:
            # Quantize bias and align it on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config


@register_quantize_target([DepthwiseBufferTempConv])
@register_aligned_inputs
@tf.keras.utils.register_keras_serializable()
class QuantizedDepthwiseBufferTempConv(DepthwiseBufferTempConv):
    """A quantized version of the DepthwiseBufferTempConv layer that operates on quantized inputs
    and weights.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    @neural_layer_init(False)
    def __init__(self, *args, quant_config=None, **kwargs):
        self.input_shift = TensorRecorder(name="input_shift")

    @tensor_inputs([FixedPoint])
    @rescale_outputs
    def call(self, inputs):
        # FIFO pop/push, shape is (B, H, W, T, C)
        self._fifo_op(inputs)
        # Align FIFO
        fifo_aligned = self._align_fifo()
        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel)
        outputs = _depthwise_buffer_temp_conv_op(fifo_aligned, kernel)
        if self.use_bias:
            # Quantize bias and align it on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config


def reset_buffers(model):
    """ Resets all FIFO-buffer of (Depthwise)BufferTempConv layers within the model.

    Args:
        model (keras.Model): the model to reset
    """
    for layer in model.layers:
        if isinstance(layer, (BufferTempConv, DepthwiseBufferTempConv)):
            layer.reset_buffer()
