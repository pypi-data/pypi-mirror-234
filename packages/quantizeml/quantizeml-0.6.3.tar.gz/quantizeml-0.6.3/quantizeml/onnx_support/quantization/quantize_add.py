import numpy as np
from ..graph_tools import array_to_tp
from ..layers import QuantizedAdd
from .outputs import downscale_fp
from .tensors import get_tensor_shape


def add_quantize_initializers(tensor_range, nodes, graph, x1_scale, x2_scale, last_block):
    def _round_pot(x):
        return 2.0**np.round(np.log2(x))
    add_node = nodes[0]
    add_name = add_node.name
    qadd = QuantizedAdd(scale=not last_block, name=add_name)
    # This quantization is feasible if and only if input scales are power-of-two
    np.testing.assert_array_equal(x1_scale, _round_pot(x1_scale), "Required a power-of-two")
    np.testing.assert_array_equal(x2_scale, _round_pot(x2_scale), "Required a power-of-two")

    # Prepare tensors list with unique names
    prefix = add_name + "_"

    # Transpose scales to align with channels
    output_name = add_node.output[0]
    output_shape = get_tensor_shape(output_name, graph)
    align_shape = [1] * (len(output_shape) - 2)
    x1_scale = x1_scale.reshape((-1, *align_shape))
    x2_scale = x2_scale.reshape((-1, *align_shape))

    # We expected input scales are a power-of-two. Take i_scale as a max of both scales
    i_scale = np.maximum(x1_scale, x2_scale)

    # Shift to apply for each input will be
    weights_dict = {prefix + "x1_shift": (i_scale / x1_scale).astype("int32"),
                    prefix + "x2_shift": (i_scale / x2_scale).astype("int32")}

    if last_block:
        out_scale = i_scale.squeeze()
    else:
        # Now consider calibrated output range
        output_range = tensor_range[output_name]
        scale, s_out, out_scale = downscale_fp(output_range, i_scale, bitwidth=8)
        # Add does not have output scale. We fold scale into shift as a power-of-two.
        # This will force an 'output scale' = 1
        s_out = 2.0**(np.log2(s_out) - np.ceil(np.log2(scale)))
        weights_dict.update({prefix + "S_out": s_out.astype(np.int32)})

    # Create node
    inputs = list(add_node.input) + list(weights_dict)
    qnode = qadd.make_node(inputs, [output_name])
    onnx_weights = array_to_tp(**weights_dict)
    return qnode, out_scale, onnx_weights


def add_convert(nodes, tensor_range, graph, scales, last_block):
    # Retrieve input scales
    num_inputs = len([x for x in nodes[0].input if x])
    if num_inputs != 2:
        raise RuntimeError("Quantization only supports 'Add' nodes with two inputs. "
                           f"Found {num_inputs} in {nodes[0].name}.")
    a_scale = scales[nodes[0].input[0]]
    b_scale = scales[nodes[0].input[1]]
    return add_quantize_initializers(tensor_range, nodes, graph, a_scale, b_scale, last_block)
