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

import tensorflow as tf

from ..layers import WeightQuantizer, OutputQuantizer, QFloatRecorder
from .record import record_quantization_variables


def check_quantization(model):
    """Checks the specified model quantization.

    It looks for errors that can be fixed in the quantization configuration:

    - inaccurate weight scales quantization,
    - saturation in integer operations.

    Args:
        model (keras.Model): the model to check

    Returns:
        list(str): the quantization issues that were detected
    """
    # First record the model variables to store qscales in output quantizers
    record_quantization_variables(model)

    messages = []
    for layer in model.layers:
        for _, attr in layer.__dict__.items():
            if isinstance(attr, OutputQuantizer):
                quantizer = attr
                range_max = quantizer.get_weights()[0]
                if tf.reduce_all(range_max == 1):
                    messages.append(f"{layer.name}/{quantizer.name} is not calibrated.")
                    continue
                # Evaluate the maximum left shift for this quantizer
                maximum_shift = quantizer.value_bits - layer.buffer_bitwidth
                # There might be a saturation in integer operations if we reached the maximum shift
                output_shift = quantizer.shift.value
                if tf.reduce_any(output_shift <= maximum_shift):
                    messages.append(f"Possible saturation detected in {layer.name}: "
                                    "try to reduce weights bits and/or scale bits.")

                # Check inaccurate weight scales quantization.
                qscales = getattr(quantizer, 'qscales', None)
                if qscales:
                    # Retrieve the original scales. They are located in the WeightQuantizer of the
                    # layer if there is one, or in all WeightQuantizer if they are several (eg.
                    # SeparableConvolution)
                    ideal_scales = None
                    for _, attr in layer.__dict__.items():
                        if (isinstance(attr, WeightQuantizer) and
                                isinstance(attr.qweights, QFloatRecorder)):
                            if ideal_scales is None:
                                ideal_scales = attr.qweights.value.scales
                            else:
                                ideal_scales *= attr.qweights.value.scales

                    if ideal_scales is not None:
                        err = tf.abs(ideal_scales - qscales.value.to_float()) / tf.abs(ideal_scales)
                        mean_err = tf.reduce_mean(err)
                        if mean_err > 5e-2:
                            message = f"Scales quantization relative error is high in " \
                                      f"{layer.name}/{quantizer.name}: {mean_err:.4f}."
                            if quantizer._axis == "per-tensor":
                                message += "Use a per-axis quantizer and/or increase scales bits."
                            else:
                                message += "Try increasing scales bits."
                            messages.append(message)
    return messages
