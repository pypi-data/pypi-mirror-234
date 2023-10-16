#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
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

__all__ = ["QuantizedReLU"]

import numpy as np
import tensorflow as tf
import keras

from .layers_base import (register_quantize_target, rescale_outputs,
                          tensor_inputs, apply_buffer_bitwidth)
from .quantizers import AlignedWeightQuantizer, OutputQuantizer
from ..tensors import FixedPoint, QFloat, QTensor


@register_quantize_target(keras.layers.ReLU)
@tf.keras.utils.register_keras_serializable()
class QuantizedReLU(keras.layers.Layer):
    """Quantized version of the ReLU activation layer applicable on FixedPoint tensor.

    Args:
        max_value (float, optional): ReLU maximum value. Defaults to 6.
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    unsupported_args = {
        'negative_slope': 0,
        'threshold': 0}

    def __init__(self, *args, max_value=6, quant_config=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.quant_config = quant_config or dict()

        # Use quant_config to build quantizers
        out_quant_cfg = self.quant_config.get("output_quantizer", False)
        if out_quant_cfg:
            self.out_quantizer = OutputQuantizer(name="output_quantizer", **out_quant_cfg)
        else:
            self.out_quantizer = None
        self.buffer_bitwidth = apply_buffer_bitwidth(self.quant_config, signed=False)
        if max_value is not None:
            # Store max_value
            if isinstance(max_value, np.ndarray):
                max_value = max_value.item()
            max_value_quantizer_cfg = self.quant_config.get("max_value_quantizer", {})
            self.max_value_quantizer = AlignedWeightQuantizer(name="max_value_quantizer",
                                                              signed=False,
                                                              **max_value_quantizer_cfg)
        self.max_value = max_value

    @tensor_inputs([QTensor])
    @rescale_outputs
    def call(self, inputs):
        """ReLU activation function.

        In other terms:

            1. clip the value between 0 and :attr:`max_value`.
            2. quantize the output if an output_quantizer is set.

        Args:
            inputs (:obj:`QFloat`): the inputs tensor.

        Returns:
            :obj:`FixedPoint`: QuantizedReLU outputs.
        """
        if isinstance(inputs, FixedPoint):
            # if inputs is FixedPoint, create an equivalent QFloat with scale
            # set to 1
            inputs = QFloat(inputs, tf.constant(1.))
        # Express zero as a QFloat aligned with the inputs because this is what the
        # dispatched operations expect.
        # The actual hardware implementation will simply use a zero integer.
        zero = QFloat(FixedPoint(tf.constant(0.), inputs.fp.value_bits, inputs.fp.frac_bits),
                      inputs.scales)

        if self.max_value is None:
            # Just remove negative values
            return tf.math.maximum(inputs, zero)
        # Quantize and align max_value with the inputs
        max_value = self.max_value_quantizer(tf.cast(self.max_value, tf.float32), inputs)
        # Clip the inputs
        return tf.clip_by_value(inputs, zero, max_value)

    def get_config(self):
        config = super().get_config()
        config.update({
            "max_value": self.max_value,
            "quant_config": self.quant_config
        })
        return config
