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
__all__ = ["get_padding_ops"]

import numpy as np

import onnx.parser
from onnx.helper import make_node


def transform_pads_into_array(pads):
    """Return the expected pads to apply in the custom operation.

    Args:
        pads (list of int): the pads to transform.

    Returns:
        TensorProto: pads as tensor.
    """
    assert len(pads) == 4, "Expect 4 values for pads"
    # ONNX Pad expect a 1D tensor of shape [2 * num_axes]. Given we should apply pads
    # over XY dimensions, others will be set to 0.
    # See https://onnx.ai/onnx/operators/onnx__Pad.html for more information.
    pads = [0, 0] + pads[:2] + [0, 0] + pads[2:]
    return np.array(pads, "int64")


def get_padding_ops(in_name, out_name, pad_value_name=""):
    """Return the pad operation chain.

    Args:
        in_name (str): the input tensor name.
        out_name (str): the required output tensor name.
        pad_value_name (str, optional): name of padding value.
            Takes a zero value when not specified. Defaults to "".

    Returns:
        list of NodeProto: the operation chain.
    """
    if not pad_value_name:
        return [make_node("Pad", inputs=[in_name, "pads"], outputs=[out_name])]

    # Knowledge: padding_value is a tensor and it contains one value per input channel.
    # Create a subgraph to map each padding value over the corresponding input channel:
    padding_subgraph = """
    agraph (float[?, 1, ?, ?] input, float[1] pval, int64[8] pads) => (float[?, 1, ?, ?] output)
    {
        output = Pad(input, pads, pval)
    }
    """
    subgraph = onnx.parser.parse_graph(padding_subgraph)

    # Perform pad operation with the steps:
    # 1. Split the input and padding value in several tensors
    # 2. Map each set of (Input[i], padding_value[i]) into the subgraph
    # 3. Concatenate all the outputs
    seq_inputs = [f"{in_name}/split", f"{pad_value_name}/split", "pads"]
    nodes = [
        make_node("SplitToSequence", [in_name], [seq_inputs[0]], axis=1),
        make_node("SplitToSequence", [pad_value_name], [seq_inputs[1]], keepdims=0),
        make_node("SequenceMap", seq_inputs, [f"{in_name}/pad"], body=subgraph),
        make_node("ConcatFromSequence", [f"{in_name}/pad"], [out_name], axis=1)
    ]
    return nodes
