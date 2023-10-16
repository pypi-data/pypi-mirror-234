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
__all__ = ["InputQuantizer", "Dequantizer"]

import numpy as np

import onnx.numpy_helper
from onnx.helper import make_node
from .base_layer import OnnxLayer
from ..graph_tools.tensor import TENSOR_SHAPE

from ..quantization.input_scale import input_zp_scale


class InputQuantizer(OnnxLayer):
    """Intermediate representation of QuantizeLinear(), use to quantize the input.

    Args:
        input_signed (bool, optional): whether the input is signed. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, input_signed=False, name=''):
        self.input_signed = input_signed
        super().__init__("Quantize", name=name)

    def __build__(self, input_ts):
        assert input_ts.dtype == np.float32

        # Add weights
        zp_dtype = "int8" if self.input_signed else "uint8"
        self._add_weight("zero_point", value=np.zeros(input_ts.shape[1]), dtype=zp_dtype)

        # Compute output shape
        output_ts = TENSOR_SHAPE(input_ts.shape, np.dtype(zp_dtype))
        return output_ts

    def quantize(self, out_tensor_range):
        # Compute output scale
        input_scale, input_zp = input_zp_scale(out_tensor_range, allow_zp=not self.input_signed)

        # Scale to set in weights is the reciprocal of ONNX calibrated one.
        scale = np.array(1 / input_scale, dtype=np.float32)

        # Save output scale and zero point (used by next layer)
        self.set_weight("scale", input_scale)
        self.set_weight("zero_point", input_zp)

        # Serialize node and weights to build the ONNX graph
        weights = [onnx.numpy_helper.from_array(scale, name=f"{self.name}/input_scale"),
                   onnx.numpy_helper.from_array(input_zp, name=f"{self.name}/input_zp")]
        node = self.make_node([x.name for x in [self.input, *weights]], [self.output.name])
        return node, weights

    @staticmethod
    def build_subgraph(op_type):
        return [make_node('QuantizeLinear', inputs=["X", "scale", "zp"], outputs=["Y"])]


class Dequantizer(OnnxLayer):
    """Intermediate representation of DequantizeLinear(), use to dequantize the input.

    Args:
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, name=''):
        super().__init__("Dequantize", name=name)

    @staticmethod
    def build_subgraph(op_type):
        return [make_node('DequantizeLinear', inputs=["X", 'scale'], outputs=["Y"])]
