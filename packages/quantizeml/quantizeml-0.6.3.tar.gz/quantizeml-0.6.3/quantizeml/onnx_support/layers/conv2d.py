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
__all__ = ["QuantizedConv2D"]

from onnx import AttributeProto as AP, TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_pool_ops, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops
from .subgraph_ops.padding import get_padding_ops


class QuantizedConv2D(OnnxLayer):
    """Intermediate representation of QLinearConv() + MaxPool() + ReLU() as an exportable node.

    Args:
        strides (list of int, optional): the convolutional strides. Defaults to [1, 1].
        pool_type (str, optional): the pool type, one of {"none", "max", "gap"}. Defaults to "none".
        pool_size (list of int, optional): the kernel pool shape.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_stride (list of int, optional): the kernel strides.
            Ignore it when pool_type != "max". Defaults to (2, 2).
        pool_pads (list of int, optional): the size of each padding dimension.
            Ignore it when pool_type != "max". Defaults to [0, 0, 0, 0].
        input_conv (bool, optional): whether it is extended the set of operations of
            the basic QuantizedConv2D, allowing to modify the padding value per input channel.
            Defaults to False.
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self,
                 strides=[1, 1],
                 pool_type="none",
                 pool_size=(2, 2),
                 pool_strides=(2, 2),
                 pool_pads=[0, 0, 0, 0],
                 input_conv=False,
                 activation=False,
                 name=''):
        assert pool_type in ["none", "max", "gap"]
        base_name = "QuantizedInputConv2D" if input_conv else "QuantizedConv2D"
        super().__init__(base_name,
                         strides=strides,
                         pool_size=pool_size,
                         pool_strides=pool_strides,
                         pool_pads=pool_pads,
                         name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["pool_type"] = pool_type
        self.serialize_attr["activation"] = activation

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias", value=0)
        self._add_weight("max_value")
        self._add_weight("pads", value=[0] * 8, dtype="int64")

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "", "W", ""]
        if "InputConv" in op_type:
            t_names[1] = "x_pad_value"
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Pad + convolution
        nodes += get_padding_ops(t_names[0], "Xi", t_names[1])
        conv_tensor_names = nodes[-1].output[:1] + t_names[2:]
        nodes.append(make_node("Conv", inputs=conv_tensor_names, outputs=["Yi"]))
        nodes[-1].attribute.append(AP(name="strides", ref_attr_name="strides", type=AP.INTS))

        # Maxpool (optional)
        if "MaxPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="MaxPool")

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # AvgPool (optional)
        if "GlobalAvgPool" in op_type:
            # Replace previous output as maxpool input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_pool_ops(nodes[-1].output[0], "Yi", pool_op_type="GlobalAvgPool")

        # Scale out (with saturation) in float domain
        shift_nodes, shift_t_names = cast_tensors_to(["Scale", "Shift"])
        nodes += shift_nodes
        nodes += get_scale_out_ops("Yi", "Yscaled", *shift_t_names)
        # Cast output to expect type
        nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        return nodes
