from pathlib import Path
import tempfile
from collections import namedtuple
import onnx
import numpy as np
from onnxruntime.quantization.quant_utils import load_model
from .calibration import calibrate
from . import conv_convert, depthwise_convert, gemm_convert, add_convert
from .input_scale import needs_zp
from ..graph_tools import nodes_to_ops_list, array_to_tp, infer_partial_io
from ..layers import AKIDA_ONNX_LAYERS, InputQuantizer, Dequantizer
from ..layers.base_layer import get_brainchip_opsetid
from ..layers.sanitize import sanitize
from .data_reader import CalibrationDataReader
from ...layers.quantization_params import QuantizationParams

# Define named tuples for QuantizerPattern and Quantizer
QuantizePattern = namedtuple('QuantizerPattern', ['pattern', 'f'])
Quantizer = namedtuple('Quantizer', ['qpattern', 'index', 'len'])

# List of supported patterns, together with matching function
PATTERNS_MAP = [
    QuantizePattern(["Conv", "Relu", "GlobalAveragePool"], conv_convert),
    QuantizePattern(["Conv", "Relu", "MaxPool"], conv_convert),
    QuantizePattern(["Conv", "GlobalAveragePool"], conv_convert),
    QuantizePattern(["Conv", "Relu"], conv_convert),
    QuantizePattern(["Conv"], conv_convert),
    QuantizePattern(["DepthwiseConv", "Relu"], depthwise_convert),
    QuantizePattern(["DepthwiseConv"], depthwise_convert),
    QuantizePattern(["Flatten", "Gemm", "Relu"], gemm_convert),
    QuantizePattern(["Flatten", "Gemm"], gemm_convert),
    QuantizePattern(["Gemm", "Relu"], gemm_convert),
    QuantizePattern(["Gemm"], gemm_convert),
    QuantizePattern(["Add"], add_convert),
]

QUANTIZED_SUFFIX = "_quantized"
DEQUANTIZED_SUFFIX = "_dequantized"


def add_dequantizer(scale, input_name):
    """
    Given a scale, create a dequantizer node and its associated scale tensor.

    Args:
        scale: scale to use for dequantizer
        input_name: name of the input to dequantize

    Returns:
        dequantizer: dequantizer node
        onnx_scale: dequantizer scale
    """
    dequantizer = Dequantizer(name=f"{input_name}/dequantize")
    # Onnx scale for dequantizer is reciprocal of akida one
    scale = np.array(scale)
    scale = (1 / scale).astype(np.float32)
    deq_name = f"{input_name}_deq_scale"
    onnx_scale = array_to_tp(**{deq_name: scale})
    qnode = dequantizer.make_node(inputs=[input_name, deq_name],
                                  outputs=[input_name + DEQUANTIZED_SUFFIX])
    return qnode, onnx_scale


def add_quantizer(tensor_range, graph):
    """
    Given a tensor range, create a quantizer node and its associated scale and
    zero point tensors.

    Args:
        tensor_range: range to use for quantizer
        graph: onnx graph

    Returns:
        quantizer: quantizer node
        weights: quantizer scale and zero point tensors
    """
    input_name = graph.input[0].name
    input_unsigned = needs_zp(input_name, graph)
    input_range = tensor_range[input_name]
    quantizer = InputQuantizer(name="quantize", input_signed=not input_unsigned)
    # Build layer
    quantizer.build(graph.input[0], out_name=input_name + QUANTIZED_SUFFIX)
    return quantizer.quantize(input_range)


def build_model(nodes, weights, input_vinfo, output_vinfo):
    """
    Given a list of nodes, weights, input value info and output value info,
    create a model and return it.

    Args:
        nodes: list of nodes
        weights: list of weights
        input_vinfo: input value info
        output_vinfo: output value info

    Returns:
        model: onnx model build from given data
    """
    graph = onnx.helper.make_graph(nodes,
                                   "quantized_model",
                                   input_vinfo,
                                   output_vinfo,
                                   initializer=weights)
    # TODO: modify this so it fills it with opset_imports from nodes
    opset_imports = [get_brainchip_opsetid(), onnx.helper.make_opsetid(
        "", onnx.defs.onnx_opset_version())]
    # Add used functions to model
    functions = []
    node_op_list = nodes_to_ops_list(nodes)
    for func in AKIDA_ONNX_LAYERS:
        if func.name in node_op_list and func not in functions:
            functions.append(func)
    # Build final model
    model = onnx.helper.make_model(graph, functions=functions, opset_imports=opset_imports)
    return model


def quantize_calibrated(target_model, tensors_range):
    """
    Given a calibrated onnx model and associated tensor ranges, create a quantized onnx
    model compatible with Brainchip's Akida IP and returns it as a new onnx model.

    Args:
        target_model: file path of model to quantize
        tensors_range: dictionary of tensor name and its range.
            Range is a tuple of min and max values.
            Example: {"input_0": (-1.23, +4.56)}

    Returns:
        quantized onnx model.
    """
    # Reject multi-input-output models (yet)
    if len(target_model.graph.input) != 1 or len(target_model.graph.output) != 1:
        raise RuntimeError("Only single input/output models are supported.")

    # Sanitize the model and make it quantization ready
    model = sanitize(target_model)

    graph = model.graph
    nodes = list(graph.node)
    ops_list = nodes_to_ops_list(nodes)

    # Split in blocks
    quantizers = []
    i = 0
    while i < len(ops_list):
        pattern_found = False
        for qpattern in PATTERNS_MAP:
            pattern = qpattern.pattern
            pat_len = len(pattern)
            if ops_list[i:i + pat_len] == pattern:
                pattern_found = True
                quantizer = Quantizer(qpattern, i, pat_len)
                quantizers.append(quantizer)
                i += pat_len
                break
        if not pattern_found:
            break

    if i == 0:
        raise RuntimeError("No quantizable pattern found")

    # Now create quantized nodes
    qnodes = []
    weights = []

    # Add quantizer at the beginning of the model
    quantizer, q_weights = add_quantizer(tensors_range, graph)
    qnodes.append(quantizer)
    weights += q_weights

    input_scales = {}
    remaining_nodes = list(target_model.graph.node)
    for quantizer in quantizers:
        block_nodes = nodes[quantizer.index:quantizer.index + quantizer.len]
        last_quantizer = quantizer == quantizers[-1]
        qnode, scale, onnx_weights = quantizer.qpattern.f(
            block_nodes, tensors_range, graph, input_scales, last_quantizer)
        input_scales[qnode.output[0]] = scale
        qnodes.append(qnode)
        weights += onnx_weights
        # Fix converted node(s) input, with output quantizer
        if qnode.input[0] == qnodes[0].input[0]:
            qnode.input[0] = qnodes[0].output[0]
        # Remove already quantized nodes in target model
        while len(remaining_nodes):
            node = remaining_nodes.pop(0)
            if node.output[0] == qnode.output[0]:
                break

    # Append a dequantizer per each partial input/output
    _, p_outputs = infer_partial_io(qnodes, exclude=[x.name for x in weights])
    p_inputs, _ = infer_partial_io(remaining_nodes, exclude=[x.name for x in graph.initializer])
    partial_outputs = set(p_outputs).union(p_inputs)
    remaining_input_info, deq_output_info = [], []
    io_dtype = onnx.TensorProto.FLOAT
    io_deq_map = []
    for out_name in partial_outputs:
        deq, deq_scale = add_dequantizer(input_scales[out_name], out_name)
        qnodes.append(deq)
        weights += deq_scale
        # Create value info for inputs and outputs (same for old and new graph)
        deq_input_tp = onnx.helper.make_tensor_value_info(deq.input[0], io_dtype, [])
        deq_output_tp = onnx.helper.make_tensor_value_info(deq.output[0], io_dtype, [])
        remaining_input_info.append(deq_input_tp)
        deq_output_info.append(deq_output_tp)
        # Create input/output map to merge quantized/float models if needed
        io_deq_map.append((deq.output[0], deq.input[0]))

    # Finally build model
    qmodel = build_model(qnodes, weights, graph.input, deq_output_info)
    if len(remaining_nodes) > 0:
        # If there were non-quantized nodes, build partial float model and merge with quantized one
        partial_inputs_weights, _ = infer_partial_io(remaining_nodes)
        remaining_weights = [w for w in graph.initializer if w.name in partial_inputs_weights]
        remaining_model = build_model(remaining_nodes,
                                      remaining_weights,
                                      remaining_input_info,
                                      graph.output)
        # Note: we would use onnx.compose helper tool to merge the models manually,
        # avoiding somes issues (e.g. topological ordering).
        qmodel = onnx.compose.merge_models(qmodel, remaining_model, io_map=io_deq_map)
    return qmodel


def quantize(model_input,
             qparams=QuantizationParams(),
             samples=None,
             num_samples=1024,
             batch_size=None):
    """
    Given an onnx model and calibration data reader, create a quantized onnx
    model compatible with Brainchip's Akida IP and returns it as a new onnx model.

    Args:

        model_input (ModelProto): the onnx model instance to quantize
        qparams (QuantizationParams, optional): Quantization parameters. It is used
            to determine if quantizing per-tensor or per-axis.
        samples (list of numpy arrays, optional): List of input samples to use for
            calibration. If not provided, random samples will be generated. Defaults
            to None.
        num_samples (int, optional): Number of samples to use for calibration.
            Defaults to 1024.
        batch_size (int, optional): Batch size to use for calibration. Defaults to
            None.

    Returns:
        quantized onnx model.
    """
    # For now only a limited QuantizationParams configuration is supported: test that
    if (
            qparams.activation_bits != 8 or
            qparams.buffer_bits != 32 or
            qparams.input_weight_bits != 8 or
            qparams.output_bits != 8 or
            qparams.weight_bits != 8):
        raise ValueError("Only default bitwidth params params qparams is allowed.")

    with tempfile.TemporaryDirectory(prefix="pre.quant.") as quant_tmp_dir:
        # To perfom ONNXRuntime optimization, we would like to use
        # onnxruntime.quantization.load_model, to optimize the model (when required)
        # and infer the intermediate shapes.
        # However, it always expects to read the model from a path. That is why we
        # save the input model if it is not a path.
        onnx.save_model(model_input, f"{quant_tmp_dir}/model.onnx")
        model_input = f"{quant_tmp_dir}/model.onnx"

        # Perform preprocessing
        model = load_model(Path(model_input), need_optimize=True)

    # Compute statistical ranges
    # Create a calibration data reader from given samples.
    calibration_data_reader = CalibrationDataReader(model, samples, num_samples, batch_size)
    tensors_range = calibrate(model,
                              calibration_data_reader,
                              per_tensor_activations=qparams.per_tensor_activations)

    qmodel = quantize_calibrated(model, tensors_range)
    return qmodel
