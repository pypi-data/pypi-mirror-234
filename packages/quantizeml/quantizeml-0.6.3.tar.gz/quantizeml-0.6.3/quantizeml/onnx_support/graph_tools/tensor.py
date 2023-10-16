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
__all__ = ["get_input_info", "array_to_tp", "infer_partial_io", "value_info_to_tensor_shape",
           "TENSOR_SHAPE"]

import numpy as np
from collections import namedtuple

import onnx
import onnx.numpy_helper

from .field import find_by_name


TENSOR_SHAPE = namedtuple('TensorShape', ['shape', 'dtype'])


def value_info_to_tensor_shape(x):
    """Helper to extract the shape and dtype contains in the input.

    Args:
        x (ValueInfoProto): the value info to read the shape.

    Returns:
        tuple: the tensor shape and dtype
    """
    tensor_type = x.type.tensor_type
    shape = tuple(el.dim_param if el.dim_param else el.dim_value for el in tensor_type.shape.dim)
    assert len(shape) > 0, f"{x.name} must have at least one dimension."
    assert all(isinstance(dim, int) for dim in shape[1:]), "Only the first dim could be null."
    dtype = onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[tensor_type.elem_type]
    return TENSOR_SHAPE(shape, dtype)


def get_input_info(graph, tensor_name=None):
    """Helper to read the shape and dtype of the graph inputs.

    Args:
        graph (GraphProto): the graph containing the tensor.
        tensor_name (str, optional): return the info only for this tensor. Defaults to None.

    Returns:
        dict or tuple: the shape and dtype of each input in the graph
    """
    shapes_and_dtypes = {}
    input_value_info = [find_by_name(tensor_name, graph.input)] if tensor_name else graph.input
    for node_info in input_value_info:
        input_name = node_info.name
        # Retrieve input shape
        tensor_shape = node_info.type.tensor_type.shape.dim
        if len(tensor_shape) == 0:
            raise RuntimeError(f"{input_name} shape must have at least one dimension.")
        input_shape = tuple(None if el.dim_param else el.dim_value for el in tensor_shape)
        assert all(dim for dim in input_shape[1:]), "Only the first dim could be null in inputs."
        # Retrieve input dtype
        input_dtype = onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[node_info.type.tensor_type.elem_type]
        shapes_and_dtypes[input_name] = (input_shape, input_dtype)

    if tensor_name:
        # Query in a specific tensor
        return shapes_and_dtypes[input_name]
    return shapes_and_dtypes


def array_to_tp(**kwargs):
    """Transform a numpy array list to TensorProto list

    Args:
        kwargs (dict, optional): a list of numpy arrays. Defaults to {}.

    Returns:
        list of TensorProto: the list of tensor proto.
    """
    # Transform each input in a TensorProto
    tensors = []
    for name, x in kwargs.items():
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        tensors.append(onnx.numpy_helper.from_array(x, name))
    return tensors


def infer_partial_io(nodes, exclude=[]):
    """Infer the partial inputs/outputs for a list of 'connected' nodes.

    Args:
        nodes (list of NodeProto): the nodes list.
        exclude (list of str): exclude tensors with these names. Defaults to [].

    Returns:
        list, list: the inputs outputs infered.
    """
    # Search partial outputs
    def _extract_unique_not_null_elems(elems, exclude=[]):
        return sorted(set(el for el in elems if el not in exclude and el), key=elems.index)

    # Infer ordered, not null and unique input/output names
    all_inputs = sum([list(node.input) for node in nodes], [])
    all_outputs = sum([list(node.output) for node in nodes], [])
    inputs = _extract_unique_not_null_elems(all_inputs, exclude=all_outputs + exclude)
    outputs = _extract_unique_not_null_elems(all_outputs, exclude=all_inputs + exclude)
    return inputs, outputs
