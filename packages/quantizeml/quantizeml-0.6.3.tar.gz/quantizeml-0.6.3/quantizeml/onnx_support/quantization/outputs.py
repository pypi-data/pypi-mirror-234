import numpy as np

from ..layers.fixed_point import to_fixed_point
from ..graph_tools import get_next_neighbor_nodes, nodes_to_ops_list
from .input_scale import input_scale_no_zp


def downscale(node, tensor_range, i_scale, graph, bitwidth=8):
    """Calculates the scale that should be applied to an integer tensor
    with i_scale to project it to a desired bitwidth.

    The following set of operations must be applied to the tensor to project it
    into the output scale:

    >>> out_tensor = tensor * scale
    >>> out_tensor = out_tensor >> log2(shift)

    Args:
        node (NodeProto): the target node.
        tensor_range (dict): the calibrate tensor range
        i_scale (np.ndarray): the input scale
        graph (GraphProto): the graph.
        bitwidth (int): the desired output width

    Returns:
        np.ndarray, np.ndarray, np.ndarray: the integer scale/shift and the new float scale
    """
    output_name = node.output[0]
    output_range = tensor_range[output_name]
    neighbor_nodes = get_next_neighbor_nodes(node, graph)
    if "Add" in nodes_to_ops_list(neighbor_nodes):
        # The multi-input layers supported in akida (such as Add) do not include a scale-in
        # operation but only a shift-in. In consequence output must be downscaled as a fixed-point.
        return downscale_fp(output_range, i_scale, bitwidth=bitwidth)
    return downscale_qf(output_range, i_scale, bitwidth)


def downscale_qf(output_range, i_scale, bitwidth=8):
    # Consider all outputs to be 8-bits, otherwise the scale would be different.
    ocalib_scale = input_scale_no_zp(output_range)
    # Divide o_calib_scale by i_scale in the same axis to obtain output scale:
    # this will consider the input scale into account.
    align_shape = [1] * (i_scale.ndim - 1)
    o_scale = ocalib_scale.reshape((-1, *align_shape)) / i_scale
    # Quantize o_scale to fit in scale + shift at 8 bit
    scale, shift = to_fixed_point(o_scale, bitwidth=bitwidth, signed=False)
    # Return shift value as a power of two
    s_out = np.array(2. ** shift, dtype=np.int32)
    return scale, s_out, ocalib_scale


def downscale_fp(output_range, i_scale, bitwidth=8):
    # Dequantize inputs in integer domain (apply scale out), multiplying by the inverse scale
    scale, in_shift = to_fixed_point(1.0 / i_scale, bitwidth=bitwidth, signed=False)
    # Compute the required output shift to come out in 8bits
    output_max = np.maximum(np.abs(output_range[0]), np.abs(output_range[1]))
    _, out_shift = to_fixed_point(output_max, bitwidth=bitwidth, signed=True)
    # Compute shift to go from in_shift to out_shift in the same axis
    # The shift can be positive (left-shift) or negative (rounded right-shift)
    align_shape = [1] * (i_scale.ndim - 1)
    shift = out_shift.reshape((-1, *align_shape)) - in_shift
    # A positive shift exceeding the target bitwidth always leads to a saturation
    np.testing.assert_array_less(shift, bitwidth,
                                 f"Cannot rescale inputs to {bitwidth} as it will saturate.")
    # In ONNX output shift is done as division (against to akida: a left shift)
    shift = np.array(2. ** -shift, dtype=np.int32)
    # Finally, outputs will have a fractional scale
    o_scale = 2.0 ** out_shift
    return scale, shift, o_scale
