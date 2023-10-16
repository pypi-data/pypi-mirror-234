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
__all__ = ["QuantizedDense1D"]

from onnx import TensorProto as TP
from onnx.helper import make_node

from .base_layer import OnnxLayer
from .subgraph_ops import cast_tensors_to, get_scale_out_ops
from .subgraph_ops.activation import get_activation_ops


class QuantizedDense1D(OnnxLayer):
    """Intermediate representation of Flatten() + QGemm() + ReLU() as an exportable node.

    Args:
        flatten (bool, optional): whether to flatten the inputs. Defaults to False.
        activation (bool, optional): whether to apply relu operation. Defaults to False.
        scale (bool, optional): whether scale the output. Defautls to True.
        name (str, optional): the node name. Defaults to ''.
    """

    def __init__(self, flatten=False, activation=False, scale=True, name=''):
        super().__init__("QuantizedDense1D", name=name)

        # Save properties need to serialize operation name
        self.serialize_attr["flatten"] = flatten
        self.serialize_attr["activation"] = activation
        self.serialize_attr["scale"] = scale

        # Declare weights
        self._add_weight("kernel")
        self._add_weight("bias")
        self._add_weight("max_value")

    @staticmethod
    def build_subgraph(op_type):
        # Cast input, weights (and bias) into float.
        t_names = ["X", "W", ""]
        if "Biased" in op_type:
            t_names[-1] = "bias"
        nodes, t_names = cast_tensors_to(t_names)

        # Flatten (optional)
        if "Flatten" in op_type:
            nodes.append(make_node("Flatten", inputs=t_names[:1], outputs=["Xflat"]))
            t_names[0] = "Xflat"

        # Gemm
        nodes.append(make_node("Gemm", inputs=t_names, outputs=["Yi"], transB=1))

        # Activation (optional)
        if "ReLU" in op_type:
            # Replace previous output as relu input
            nodes[-1].output.__setitem__(0, nodes[-1].op_type)
            nodes += get_activation_ops(nodes[-1].output[0], "Yi", "ReLUClipped" in op_type)

        # Apply final scale (with saturation) (optional)
        if "Scaled" in op_type:
            shift_nodes, shift_t_names = cast_tensors_to(["Scale", "Shift"])
            nodes += shift_nodes
            nodes += get_scale_out_ops("Yi", "Yscaled", *shift_t_names, saturate=True)
            nodes.append(make_node("Cast", ["Yscaled"], ["Y"], to=TP.INT8))
        else:
            nodes.append(make_node("Cast", ["Yi"], ["Y"], to=TP.INT32))
        return nodes
