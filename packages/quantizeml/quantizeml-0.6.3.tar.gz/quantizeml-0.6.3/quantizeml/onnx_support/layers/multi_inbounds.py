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
__all__ = ["QuantizedAdd"]

from onnx import TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_scale_out_ops, get_input_shift_ops


class QuantizedAdd(OnnxLayer):
    """Intermediate representation of Add() as an exportable node."""

    def __init__(self, scale=True, name=''):
        super().__init__("QuantizedAdd", name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["scale"] = scale

    @staticmethod
    def build_subgraph(op_type):
        # Cast inputs and shift to float.
        nodes, t_names = cast_tensors_to(["X", "Y", "Xs", "Ys"])

        # Align inputs with input shift
        nodes += get_input_shift_ops(t_names[0], t_names[2], "Xshifted")
        nodes += get_input_shift_ops(t_names[1], t_names[3], "Yshifted")

        # Perform addition
        nodes.append(make_node("Add", inputs=["Xshifted", "Yshifted"], outputs=["Zi"]))

        # Apply final output shift (optional)
        if "Scaled" in op_type:
            shift_nodes, shift_t_names = cast_tensors_to(["", "Shift"])
            nodes += shift_nodes
            nodes += get_scale_out_ops("Zi", "Zscaled", *shift_t_names)
            nodes.append(make_node("Cast", ["Zscaled"], ["Z"], to=TP.INT8))
        else:
            nodes.append(make_node("Cast", ["Zi"], ["Z"], to=TP.INT32))
        return nodes
