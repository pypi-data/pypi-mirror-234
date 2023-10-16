import numpy as np
from ..graph_tools import get_variable, get_node, array_to_tp
from ..layers.dense import QuantizedDense1D
from .weights import quantize_weights, quantize_value_shift
from .input_scale import input_scale_no_zp
from .outputs import downscale
from .tensors import get_tensor_shape


def gemm_has_bias(gemm_node):
    # If third attribute is there and it is not empty, then there is a bias
    if len(gemm_node.input) == 3 and gemm_node.input[2]:
        return True
    return False


def get_qgemm(nodes, graph, output_32_bit):
    gemm_node = get_node(nodes, 'Gemm')
    assert gemm_node is not None
    flatten = bool(get_node(nodes, 'Flatten'))
    act_node = get_node(nodes, 'Relu')
    qgemm = QuantizedDense1D(flatten=flatten,
                             activation=bool(act_node),
                             scale=not output_32_bit,
                             name=gemm_node.name)

    # Sets the weights to configure the operation chain
    qgemm.set_weight("kernel", get_variable(gemm_node.input[1], graph))
    if gemm_has_bias(gemm_node):
        qgemm.set_weight("bias", get_variable(gemm_node.input[2], graph))
    if act_node and len(act_node.input) > 2 and act_node.input[2]:
        qgemm.set_weight("max_value", get_variable(act_node.input[2], graph))
    return qgemm


def gemm_quantize_initializers(qgemm,
                               tensor_range,
                               nodes,
                               graph,
                               i_scale,
                               output_32_bit):
    gemm_node = get_node(nodes, 'Gemm')
    kernel = qgemm.weights["kernel"]
    filters, channels = kernel.shape

    # Rescale kernel according to input scale. This operation is different if
    # pattern contain a Flatten.
    i_scale = np.array(i_scale)
    assert i_scale.ndim <= 1
    if 'Flatten' in qgemm.op_type:
        flatten_node = get_node(nodes, 'Flatten')
        # If flatten is there, we need to reshape weights to apply input scale
        _, c, x, y = get_tensor_shape(flatten_node.input[0], graph)
        # Unroll first flattened inputs
        kernel = np.reshape(kernel, (filters, c, x, y))
        # Reshape to allow kernel division
        if i_scale.ndim == 1:
            i_scale = i_scale.reshape((1, c, 1, 1))
        # Divide kernel by input shape (that has shape of c)
        kernel = kernel / i_scale
        # Reshape back to original shape
        kernel = np.reshape(kernel, (filters, channels))
    else:
        # For now only support 1D dense
        input_shape = get_tensor_shape(gemm_node.input[0], graph)
        assert len(input_shape) == 2, "Only 1D input supported for now"
        kernel = kernel / i_scale

    # Quantize and set weights and bias
    bias = qgemm.weights["bias"]
    if np.size(bias) == 0:
        bias = 0
    qweights, qbias, i_scale = quantize_weights(kernel, bias)

    # Prepare tensors list with unique names
    gemm_name = gemm_node.name
    prefix = gemm_name + "_"
    weights_dict = {prefix + "Wi": qweights}
    if "Biased" in qgemm.op_type:
        weights_dict[prefix + "B"] = qbias

    # Quantize max value when there is an activation
    if "Clipped" in qgemm.op_type:
        qmax_value = quantize_value_shift(qgemm.weights["max_value"], i_scale, signed=False)
        weights_dict[prefix + "max_value"] = qmax_value

    if output_32_bit:
        output_scale = i_scale
    else:
        # Now consider calibrated output range
        scale, s_out, output_scale = downscale(nodes[-1], tensor_range, i_scale, graph)
        # Add scale out inputs and weights
        weights_dict[prefix + "M"] = scale
        weights_dict[prefix + "S_out"] = s_out

    # Create node
    inputs = nodes[0].input[:1] + list(weights_dict)
    qnode = qgemm.make_node(inputs, nodes[-1].output)
    onnx_weights = array_to_tp(**weights_dict)

    return qnode, output_scale, onnx_weights


def gemm_convert(nodes, tensor_range, graph, scales, last_block):
    qgemm = get_qgemm(nodes, graph, last_block)
    input_name = nodes[0].input[0]
    i_scale = scales.get(input_name, None)
    if i_scale is None:
        input_range = tensor_range[input_name]
        i_scale = input_scale_no_zp(input_range)
    return gemm_quantize_initializers(qgemm, tensor_range,
                                      nodes, graph, i_scale, last_block)
