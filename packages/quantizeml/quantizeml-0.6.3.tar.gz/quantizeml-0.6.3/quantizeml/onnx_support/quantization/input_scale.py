import numpy as np
from .tensors import get_tensor_shape
# Akida inputs/outputs range is [-127, 127], int8 for hidden layers
AKIDA_IO_MAX = 127.0


def needs_zp(input_name, graph):
    input_shape = get_tensor_shape(input_name, graph)
    first_node_input_match = input_name == graph.input[0].name
    first_op_type = graph.node[0].op_type

    # Model may have zero point if input op is conv and channel numbers is one of [1, 3].
    # Note: shape format is (batch,C,X,Y).
    return first_op_type == 'Conv' and first_node_input_match and input_shape[1] in (1, 3)


def _input_conv_zp_scale(input_range):
    assert len(input_range) == 2, "Expected (min, max) in input_range."
    rmin, rmax = input_range
    if np.any(rmin >= rmax):
        raise ValueError("Invalid input range")
    # input is uint8, so max is 255. Hence we can deduce the scale
    # Note that akida_scale is reciprocal of onnx scale
    akida_scale = 255 / (rmax - rmin)
    zero_point = -np.round(rmin * akida_scale)
    # In hardware we cannot handle negative zero point. But a negative zero point is
    # a consequence of an input WITH POSITIVE RANGE. For this case, we can quantize assuming
    # a symmetric range between [-rmax, rmax] (rmin = 0).
    akida_scale = np.where(zero_point < 0, 255 / rmax, akida_scale)
    zero_point = np.maximum(0, zero_point)
    return akida_scale, np.array(zero_point, np.uint8)


def input_scale_no_zp(input_range):
    assert len(input_range) == 2, "Expected (min, max) in input_range."
    rmin, rmax = input_range
    if np.any(rmin > rmax):
        raise ValueError("Invalid input range")
    rmax = np.maximum(np.abs(rmin), np.abs(rmax))
    # Replace rmax == 0 by an epsilon to avoid division by zero
    rmax = np.maximum(rmax, 1e-7)
    # input is int8, so max is AKIDA_IO_MAX. Hence we can deduce the scale
    # Note that akida_scale is reciprocal of onnx scale
    akida_scale = AKIDA_IO_MAX / rmax
    return akida_scale


def input_zp_scale(input_range, allow_zp=False):
    """Compute the input scale and zero point """
    if allow_zp:
        i_scale, zero_point = _input_conv_zp_scale(input_range)
    else:
        # this will be like an input data + conv, no zero point
        # Note: To force signed QuantizeLinear outputs, we return an int8 zero point
        i_scale = input_scale_no_zp(input_range)
        zero_point = np.zeros_like(i_scale, dtype=np.int8)
    return np.array(i_scale, "float32"), zero_point
