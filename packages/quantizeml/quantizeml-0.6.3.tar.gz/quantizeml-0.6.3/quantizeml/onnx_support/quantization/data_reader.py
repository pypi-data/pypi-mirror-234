__all__ = ["CalibrationDataReader"]

import numpy as np
import warnings

import onnx
from onnxruntime.quantization import CalibrationDataReader as _CalibrationDataReader

from ..graph_tools import get_input_info


def gen_random_samples(input_shape, dtype="float32"):
    output_type = np.dtype(dtype)
    if issubclass(output_type.type, np.integer):
        iinfo = np.iinfo(output_type)
        return np.random.randint(iinfo.min, iinfo.max, input_shape, dtype=dtype)
    return np.random.uniform(-1.0, 1.0, input_shape).astype(dtype)


class CalibrationDataReader(_CalibrationDataReader):
    """Object to read or generate a set of samples to calibrate an ONNX model to be quantized.

    If samples are not specified, generate random samples in the range of [-1, 1]
    when input model type is float, otherwise infer ranges.

    Common use mode:
    >>> dr = CalibrationDataReader(onnx_path, num_samples=10, batch_size=1)
    >>> sample = dr.get_next()
    >>> assert sample[dr.inputs_name].shape[0] == 1
    >>> assert sample[dr.inputs_name].min() >= -1
    >>> assert sample[dr.inputs_name].max() <= 1

    Args:
        model (str or ModelProto): the ONNX model (or its path) to be calibrated.
        samples (str or np.ndarray, optional): the samples (or its path) to process.
            If not provided, generate random samples following the model input shape
            and the batch_size attribute. Defaults to None.
        num_samples (int, optional): the number of samples to generate.
            Ignore it if samples are provided. Defaults to None.
        batch_size (int, optional): split samples in batches.
            Overwrite it when the model has static inputs. Defaults to 1.
    """

    def __init__(self,
                 model,
                 samples=None,
                 num_samples=None,
                 batch_size=1):

        model, samples = _read_model_samples(model, samples)
        self.inputs_name = model.graph.input[0].name

        # Set mandatory batch size when model is not batchable
        input_shape, input_type = get_input_info(model.graph, tensor_name=self.inputs_name)
        self.batch_size = input_shape[0] or batch_size or 1

        # Generate random samples if needed
        if samples is None:
            if num_samples is None:
                raise ValueError("Either samples or num_samples must be specified")
            samples = gen_random_samples((num_samples, *input_shape[1:]), input_type)
        if input_shape[0] is not None:
            # Truncate samples to fit model batch size
            N = (samples.shape[0] // self.batch_size) * self.batch_size
            if N != samples.shape[0]:
                warnings.warn("Truncating samples to fit model batch size "
                              f"({N} instead of {samples.shape[0]}).")
                samples = samples[:N]
        self.dataset = samples

        # Verify that dataset type is the same as the model input type
        assert self.dataset.dtype == input_type, "Samples type does not match with model input one."

        # Process samples
        self.index = 0
        self.num_samples = self.dataset.shape[0] / self.batch_size

        # Check samples are the expected model shape
        if self.dataset.shape[1:] != input_shape[1:]:
            raise RuntimeError("Samples shape does not match model input shape. "
                               f"Please verify samples are compatible with {input_shape}.")

    def get_next(self):
        if self.index >= self.num_samples:
            print(f"\rCalibrating with {self.index}/{self.num_samples} samples", end="")
            return print()

        sample = self.dataset[self.index * self.batch_size:(self.index + 1) * self.batch_size]
        self.index += 1
        return {self.inputs_name: sample}

    def rewind(self):
        self.index = 0


def _read_model_samples(model, samples):
    if isinstance(samples, str):
        data = np.load(samples)
        samples = np.concatenate([data[item] for item in data.files])
    if isinstance(model, str):
        model = onnx.load_model(model)

    assert len(model.graph.input) == 1, "multi-input are not supported models yet"
    assert len(model.graph.output) == 1, "multi-outputs are not supported models yet"
    assert isinstance(samples, np.ndarray) or samples is None, f"Unrecognized samples {samples}"
    return model, samples
