import uuid
import tempfile
from copy import deepcopy
from pathlib import Path
import numpy as np

import onnx
from onnx import numpy_helper as np_onnx, TensorProto as TP
from onnx.helper import make_node, make_tensor_value_info, make_attribute

from onnxruntime.quantization.registry import QLinearOpsRegistry
from onnxruntime.quantization import MinMaxCalibrater
from onnxruntime.quantization.quant_utils import clone_model_with_shape_infer

from ..graph_tools import get_op_version, find_by_name


def _get_tensor_rank(tensor_name, value_infos):
    value_info = find_by_name(tensor_name, list(value_infos.values()))
    return len(value_info.type.tensor_type.shape.dim)


class MinMaxOutputCalibrater(MinMaxCalibrater):
    """Calibrable method that extends MinMaxCalibrater functions, allowing calibration per axis
    on activations when required.

    Args:
        model (ModelProto or str): the ONNX model to calibrate.
        activation_per_tensor (bool, optional): whether to calibrate per tensor.
            Defaults to True.
        op_types_to_calibrate (list of str, optional): operator types to calibrate.
            By default, calibrate all the float32/float16 tensors.
        augmented_model_path (str, optional): save augmented model to this path.
            Defaults to "augmented_model.onnx".
        symmetric (bool, optional): make range of tensor symmetric (central point is 0).
            Defaults to False.
        use_external_data_format (bool, optional): use external data format to store model
            which size is >= 2Gb. Defaults to False.
        moving_average (bool, optional): compute the moving average of the minimum and maximum
            values instead of the global minimum and maximum. Defaults to False.
        averaging_constant (float, optional): constant smoothing factor to use
            when computing the moving average. Defaults to 0.01
        per_tensor_activations (bool, optional): wheter to compute activation ranges per tensor.
            Defaults to True.
    """

    def __init__(self, *args, per_tensor_activations=True, **kwargs):
        self.per_tensor_activations = per_tensor_activations
        super().__init__(*args, **kwargs)
        self.model_original_inputs = set(x.name for x in self.model.graph.input)

    def augment_graph(self):
        """ Adds ReduceMin and ReduceMax nodes to all quantization_candidates op type nodes in
        model and ensures their outputs are stored as part of the graph output
        """
        model = clone_model_with_shape_infer(self.model)

        tensors, value_infos = self.select_tensors_to_calibrate(model)
        # Add inputs even if the model does not start with a node to calibrate
        tensors.update([el.name for el in self.model.graph.input])
        reduce_axes_name = str(uuid.uuid4())
        # Channels are in 2nd dimension and we support only 2D/4D tensors for now.
        reduce_axes = np_onnx.from_array(np.array([0, 2, 3], dtype=np.int64), reduce_axes_name)
        is_some_per_axis = False

        def add_reduce_min_max(tensor_name, reduce_op_name):
            nonlocal is_some_per_axis

            # Adding reduce operation node
            reduce_output = tensor_name + "_" + reduce_op_name
            reduce_node = make_node(reduce_op_name,
                                    [tensor_name],
                                    [reduce_output],
                                    keepdims=0,
                                    name=reduce_output)

            # We only support calibration per axis if tensor is 4D and is not the input
            tensor_rank = _get_tensor_rank(tensor_name, value_infos)
            if tensor_rank == 4 and not self.per_tensor_activations:
                tensor_out_shape = [None]
                # Depending of the onnx opset version, axes in ReduceMin/ReduceMax
                # are in attribute or inputs:
                if get_op_version(reduce_op_name, model) < 18:
                    reduce_node.attribute.append(make_attribute("axes", [0, 2, 3]))
                else:
                    reduce_node.input.append(reduce_axes_name)
                    is_some_per_axis = True
            else:
                tensor_out_shape = []
            model.graph.node.append(reduce_node)

            # Make sure reduce operation will be an output of the graph
            reduce_value_info = make_tensor_value_info(reduce_output, TP.FLOAT, tensor_out_shape)
            model.graph.output.append(reduce_value_info)

        for tensor in tensors:
            add_reduce_min_max(tensor, "ReduceMin")
            add_reduce_min_max(tensor, "ReduceMax")

        # If some node is calibrated per axis, save reduce axes tensor on graph
        if is_some_per_axis:
            model.graph.initializer.append(reduce_axes)

        # Save temporal model
        onnx.save(model,
                  self.augmented_model_path,
                  save_as_external_data=self.use_external_data_format)
        self.augment_model = model

    def compute_range(self):
        """ Compute the min-max range of tensor.

        Shameful copy of super().compute_range(), handling per axis tensors

        Returns:
            dict: tensor names with min-max ranges.
        """

        if len(self.intermediate_outputs) == 0:
            return self.calibrate_tensors_range

        output_names = [self.infer_session.get_outputs()[i].name
                        for i in range(len(self.intermediate_outputs[0]))]
        output_dicts_list = [dict(zip(output_names, intermediate_output))
                             for intermediate_output in self.intermediate_outputs]

        merged_output_dict = {}
        for d in output_dicts_list:
            for k, v in d.items():
                merged_output_dict.setdefault(k, []).append(v)
        added_output_names = output_names[self.num_model_outputs:]
        calibrate_tensor_names = [added_output_names[i].rpartition("_")[0]
                                  for i in range(0, len(added_output_names), 2)]

        merged_output_dict = dict((i, merged_output_dict[i])
                                  for i in merged_output_dict
                                  if i not in self.model_original_outputs)

        pairs = []
        for i in range(0, len(added_output_names), 2):
            if self.moving_average:
                min_value = np.mean(merged_output_dict[added_output_names[i]], axis=0)
                max_value = np.mean(merged_output_dict[added_output_names[i + 1]], axis=0)
            else:
                min_value = np.min(merged_output_dict[added_output_names[i]], axis=0)
                max_value = np.max(merged_output_dict[added_output_names[i + 1]], axis=0)

            if self.symmetric:
                max_absolute_value = np.max([np.abs(min_value), np.abs(max_value)], axis=0)
                pairs.append(tuple([-max_absolute_value, max_absolute_value]))
            else:
                pairs.append(tuple([min_value, max_value]))

        new_calibrate_tensors_range = dict(zip(calibrate_tensor_names, pairs))
        if self.calibrate_tensors_range:
            self.calibrate_tensors_range = self.merge_range(
                self.calibrate_tensors_range, new_calibrate_tensors_range)
        else:
            self.calibrate_tensors_range = new_calibrate_tensors_range
        return self.calibrate_tensors_range


def calibrate(model,
              calibration_data_reader,
              symmetric=False,
              average=False,
              per_tensor_activations=True):
    """Given an onnx model and calibration data reader, create a calibrator to
    obtain tensor ranges used for calibration.

    Args:
        model (ModelProto): onnx model to calibrate
        calibration_data_reader (CalibrationDataReader): a calibration data reader. It
            enumerates calibration data and generates inputs for the original model.
        symmetric (bool, optional): whether the final range of tensor during calibration
            will be explicitly set to symmetric to central point "0". Defaults to False.
        average (bool, optional): whether average of the minimum and maximum values
            will be computed. Defaults to False.
        per_tensor_activations (bool, optional): wheter to compute activation ranges per tensor.
            Defaults to True.

    Returns:
        dict: tensor names with calibration ranges.
    """
    with tempfile.TemporaryDirectory(prefix="ort.quant.") as quant_tmp_dir:
        # Declare MinMax calibrator, cloning model to avoid modifying the original one
        # Note: collect_data() and compute_range() are called just one time.
        # Therefore, moving average only performs an average of the minimum and maximum values.
        calibrator = MinMaxOutputCalibrater(
            deepcopy(model),
            op_types_to_calibrate=list(QLinearOpsRegistry.keys()),
            augmented_model_path=Path(quant_tmp_dir).joinpath("augmented_model.onnx").as_posix(),
            use_external_data_format=False,
            symmetric=symmetric,
            moving_average=average,
            per_tensor_activations=per_tensor_activations)

        # Augment model with MinMax nodes and create interface
        calibrator.augment_graph()
        calibrator.create_inference_session()

        # Collect output tensors with calibration data and compute range
        calibrator.collect_data(calibration_data_reader)
        tensors_range = calibrator.compute_range()
        del calibrator
    return tensors_range
