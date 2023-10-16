from ..graph_tools import find_by_name


def get_tensor_shape(tensor_name, graph):
    """Helper to read the shape of one tensor.

    Args:
        tensor_name (str): the tensor to read the shape.
        graph (GraphProto): the graph containing the tensor.

    Returns:
        tuple of ints: the tensor shape
    """
    value_info = list(graph.value_info) + list(graph.input) + list(graph.output)
    node_info = find_by_name(tensor_name, value_info)
    if not node_info:
        raise RuntimeError(f"Element with name {tensor_name} not found in graph value info. "
                           "Before calling this function, run infer_shapes().")

    tensor_shape = node_info.type.tensor_type.shape.dim
    if len(tensor_shape) == 0:
        raise RuntimeError(f"{tensor_name} shape must have at least one dimension. "
                           "Make sure infer_shapes() was called previously.")
    input_shape = tuple(None if el.dim_param else el.dim_value for el in tensor_shape)
    assert all(dim for dim in input_shape[1:]), "Only the first dim could be null."
    return input_shape
