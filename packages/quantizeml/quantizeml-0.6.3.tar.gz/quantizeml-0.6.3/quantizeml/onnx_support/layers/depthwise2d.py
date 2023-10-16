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
__all__ = ["QuantizedDepthwise2D"]

from onnx import AttributeProto as AP, TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .subgraph_ops.padding import get_padding_ops


class QuantizedDepthwise2D(OnnxLayer):
    """Intermediate representation of Conv() + MaxPool() + ReLU() as an exportable node.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        groups (int, optional): the number of groups input channels and
            output channels are divided into. Defaults to 1.
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, strides=[1, 1], groups=1, activation=False, name=''):
        # Serialize attributes in operation name
        super().__init__("QuantizedDepthwise2D", groups=groups, strides=strides, name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["activation"] = activation

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")
        self._add_weight("pads", value=[0] * 8, dtype="int64")

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Pad + convolution
        nodes += get_padding_ops(t_names[0], "Xi")
        t_names[0] = "Xi"
        nodes.append(make_node("Conv", inputs=t_names, outputs=["Yi"]))
        # Constrain attribute that we allow
        nodes[-1].attribute.extend([AP(name="strides", ref_attr_name="strides", type=AP.INTS),
                                   AP(name="group", ref_attr_name="groups", type=AP.INT)])

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Scale out (with saturation) in float domain
        shift_nodes, shift_t_names = cast_tensors_to(["Scale", "Shift"])
        nodes += shift_nodes
        nodes += get_scale_out_ops("Yi", "Yscaled", *shift_t_names)
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes
