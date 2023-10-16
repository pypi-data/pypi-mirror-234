import numpy as np
from ..graph_tools import get_field, get_variable, get_node, array_to_tp
from ..layers.conv2d import QuantizedConv2D
from ..layers.subgraph_ops.padding import transform_pads_into_array
from .weights import quantize_weights, quantize_value_shift
from .input_scale import input_zp_scale, needs_zp
from .outputs import downscale
from .tensors import get_tensor_shape


def conv_has_bias(conv_node):
    # If third attribute is there and it is not empty, then there is a bias
    if len(conv_node.input) == 3 and conv_node.input[2]:
        return True
    return False


def get_qconv(nodes, graph, is_input_conv=False):
    conv_node = nodes[0]
    assert conv_node.op_type == 'Conv'
    strides = get_field(conv_node, 'strides', (1, 1))

    pool_type = "none"
    pool_size = (2, 2)
    pool_strides = (1, 1)
    pool_node = get_node(nodes, 'MaxPool')
    pool_pads = [0, 0, 0, 0]
    if pool_node:
        pool_type = "max"
        # kernel_shape attribute is mandatory for MaxPool
        pool_size = get_field(pool_node, 'kernel_shape')
        pool_strides = get_field(pool_node, 'strides', pool_strides)
        pool_pads = get_field(pool_node, "pads", pool_pads)
    pool_node = get_node(nodes, 'GlobalAveragePool')
    if pool_node:
        pool_type = "gap"

    act_node = get_node(nodes, 'Relu')
    qconv = QuantizedConv2D(strides=strides,
                            pool_type=pool_type,
                            pool_size=pool_size,
                            pool_strides=pool_strides,
                            pool_pads=pool_pads,
                            activation=bool(act_node),
                            input_conv=is_input_conv,
                            name=conv_node.name)

    # Sets the weights to configure the operation chain
    qconv.set_weight("kernel", get_variable(conv_node.input[1], graph))
    if conv_has_bias(conv_node):
        qconv.set_weight("bias", get_variable(conv_node.input[2], graph))
    pads = get_field(conv_node, 'pads', False)
    if pads:
        qconv.set_weight("pads", transform_pads_into_array(pads))
    if act_node and len(act_node.input) > 2 and act_node.input[2]:
        qconv.set_weight("max_value", get_variable(act_node.input[2], graph))
    return qconv


def conv_quantize_initializers(qconv, tensor_range, nodes, graph, i_scale,
                               zero_point=0):
    conv_node = nodes[0]
    if np.any(zero_point != 0) and "InputConv" not in qconv.op_type:
        raise RuntimeError(f"Invalid quantization on {conv_node.name}: "
                           "only QuantizedInputConv allows zero point different from zero.")

    # Perform cross-layer equalization, i.e.: rescale weights with input scale.
    # To do that first reshape i_scale to put last two dimensions to 1 and be
    # capable of broadcasting.
    i_scale = np.array(i_scale)
    assert i_scale.ndim <= 1
    i_scale = i_scale.reshape((-1, 1, 1))
    kernel = qconv.weights["kernel"] / i_scale
    # Quantize and set weights and bias
    bias = qconv.weights["bias"]
    qweights, qbias, i_scale = quantize_weights(kernel, bias, zero_point)
    # Reshape scale to match with channel axis
    i_scale = i_scale.reshape((-1, 1, 1))

    # Prepare tensors list with unique names
    conv_name = conv_node.name
    prefix = conv_name + "_"
    weights_dict = {}
    if "InputConv" in qconv.op_type:
        # If calibration was done per tensor, repeat zero point over each channel
        if zero_point.size == 1:
            zero_point = np.repeat(zero_point, kernel.shape[1])
        weights_dict[prefix + "Xpad"] = zero_point
    weights_dict[prefix + "Wi"] = qweights
    if "Biased" in qconv.op_type:
        weights_dict[prefix + "B"] = qbias
    weights_dict[prefix + "pads"] = qconv.weights["pads"]

    # Quantize max value when there is an activation
    if "Clipped" in qconv.op_type:
        qmax_value = quantize_value_shift(qconv.weights["max_value"], i_scale, signed=False)
        weights_dict[prefix + "max_value"] = qmax_value

    # Fold spatial dimension when GAP
    if "GlobalAvgPool" in qconv.op_type:
        input_shape = get_tensor_shape(conv_node.output[0], graph)
        i_scale *= input_shape[-2] * input_shape[-1]

    # Now consider calibrated output range
    scale, s_out, ocalib_scale = downscale(nodes[-1], tensor_range, i_scale, graph)
    weights_dict.update({prefix + "M": scale, prefix + "S_out": s_out})

    # Create node
    inputs = conv_node.input[:1] + list(weights_dict)
    qnode = qconv.make_node(inputs, nodes[-1].output)
    onnx_weights = array_to_tp(**weights_dict)

    return qnode, ocalib_scale, onnx_weights


def conv_convert(nodes, tensor_range, graph, scales, _last_block):
    conv_node = nodes[0]
    input_name = conv_node.input[0]
    i_scale = scales.get(input_name, None)
    if i_scale is None:
        input_range = tensor_range[input_name]
        allow_zp = needs_zp(input_name, graph)
        i_scale, zero_point = input_zp_scale(input_range, allow_zp)
    else:
        zero_point = np.array(0, dtype=np.int8)

    qconv = get_qconv(nodes, graph, is_input_conv=zero_point.dtype == np.uint8)
    return conv_quantize_initializers(qconv, tensor_range,
                                      nodes, graph, i_scale, zero_point)
