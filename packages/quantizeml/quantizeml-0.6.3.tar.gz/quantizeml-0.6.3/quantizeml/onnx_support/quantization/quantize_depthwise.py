import numpy as np
from ..graph_tools import get_field, get_variable, get_node, array_to_tp
from ..layers.subgraph_ops.padding import transform_pads_into_array
from ..layers import QuantizedDepthwise2D
from .weights import quantize_weights, quantize_value_shift
from .input_scale import input_scale_no_zp
from .outputs import downscale


def dw_has_bias(conv_node):
    # If third attribute is there and it is not empty, then there is a bias
    return len(conv_node.input) == 3 and conv_node.input[2]


def get_qdepthwise(nodes, graph):
    dw_node = nodes[0]
    assert dw_node.op_type == 'DepthwiseConv'
    strides = get_field(dw_node, 'strides', (1, 1))
    groups = get_field(dw_node, 'group')
    act_node = get_node(nodes, 'Relu')

    qdepthwise = QuantizedDepthwise2D(strides=strides,
                                      groups=groups,
                                      activation=bool(act_node),
                                      name=dw_node.name)

    # Sets the weights to configure the operation chain
    qdepthwise.set_weight("kernel", get_variable(dw_node.input[1], graph))
    if dw_has_bias(dw_node):
        qdepthwise.set_weight("bias", get_variable(dw_node.input[2], graph))
    pads = get_field(dw_node, 'pads', False)
    if pads:
        qdepthwise.set_weight("pads", transform_pads_into_array(pads))
    if act_node and len(act_node.input) > 2 and act_node.input[2]:
        qdepthwise.set_weight("max_value", get_variable(act_node.input[2], graph))
    return qdepthwise


def depthwise_quantize_initializers(qdepthwise, tensor_range, nodes, graph, i_scale):
    dw_node = nodes[0]

    # Perform cross-layer equalization, i.e.: rescale weights with input scale.
    # To do that first reshape i_scale to put last dimensions to 1 and be capable of broadcasting.
    # Note in depthwise the kernel shape is (F=C, 1, Kx, Ky).
    i_scale = np.array(i_scale)
    assert i_scale.ndim <= 1
    i_scale = i_scale.reshape((-1, 1, 1, 1))
    kernel = qdepthwise.weights["kernel"] / i_scale
    # Quantize and set weights and bias
    bias = qdepthwise.weights["bias"]
    if np.size(bias) == 0:
        bias = 0
    qweights, qbias, i_scale = quantize_weights(kernel, bias)
    # Reshape scale to match with channel axis
    i_scale = i_scale.reshape((-1, 1, 1))

    # Prepare tensors list with unique names
    dw_name = dw_node.name
    prefix = dw_name + "_"
    weights_dict = {prefix + "Wi": qweights}
    if "Biased" in qdepthwise.op_type:
        weights_dict[prefix + "B"] = qbias
    weights_dict[prefix + "pads"] = qdepthwise.weights["pads"]

    # Quantize max value when there is an activation
    if "Clipped" in qdepthwise.op_type:
        qmax_value = quantize_value_shift(qdepthwise.weights["max_value"], i_scale, signed=False)
        weights_dict[prefix + "max_value"] = qmax_value

    # Now consider calibrated output range
    scale, s_out, o_scale = downscale(nodes[-1], tensor_range, i_scale, graph)
    weights_dict.update({prefix + "M": scale, prefix + "S_out": s_out})

    # Create node
    inputs = dw_node.input[:1] + list(weights_dict)
    qnode = qdepthwise.make_node(inputs, nodes[-1].output)
    onnx_weights = array_to_tp(**weights_dict)

    return qnode, o_scale, onnx_weights


def depthwise_convert(nodes, tensor_range, graph, scales, _last_block):
    qdepthwise = get_qdepthwise(nodes, graph)
    input_name = nodes[0].input[0]
    i_scale = scales.get(input_name, None)
    if i_scale is None:
        input_range = tensor_range[input_name]
        i_scale = input_scale_no_zp(input_range)
    return depthwise_quantize_initializers(qdepthwise, tensor_range, nodes, graph, i_scale)
