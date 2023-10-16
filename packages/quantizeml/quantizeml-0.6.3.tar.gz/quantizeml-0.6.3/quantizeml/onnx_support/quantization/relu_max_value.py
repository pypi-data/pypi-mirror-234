
from ..graph_tools import get_variable, get_node
from .weights import quantize_value_shift


def quantize_relu_max_value(nodes, i_scale, graph):
    """
    Quantize the max value of the Relu node if it is determined.
    """
    act_node = get_node(nodes, 'Relu')
    qmax_value = None
    if act_node and len(act_node.input) > 2 and act_node.input[2]:
        max_value = get_variable(act_node.input[2], graph)
        qmax_value = quantize_value_shift(max_value, i_scale, signed=False)
    return qmax_value
