#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

__all__ = ["quantize", "dump_config"]

import warnings

from keras import Model, layers
from onnx import ModelProto

from .utils import deep_clone_model
from .transforms import insert_layer, sanitize
from .calibrate import calibrate
from ..layers import (OutputQuantizer, WeightQuantizer, Dequantizer, quantization,
                      QuantizationParams, get_quantization_params, Attention, QuantizedConv2D,
                      QuantizedDepthwiseConv2D, QuantizedSeparableConv2D, QuantizedDense)
from ..layers.layers_base import (_GLOBAL_LAYER_TO_QLAYER, _GLOBAL_NO_OUTPUT_QUANTIZER,
                                  _GLOBAL_ALIGNED_INPUTS)
from ..onnx_support.quantization.quantize import quantize as quantize_onnx


# List of Quantizer layer's that do not have a float layer representation
NO_FLOAT_CUSTOM_QLAYERS = [Dequantizer, OutputQuantizer, WeightQuantizer]


def get_quantized_layer(layer):
    """ Returns the quantized version of the layer.

    Args:
        layer (keras.layers.Layer): layer of interest

    Returns:
        keras.layer: quantized version of the layer if it exists, None otherwise.
    """
    return _GLOBAL_LAYER_TO_QLAYER.get(layer.__class__.__name__, None)


def is_quantized_layer(layer):
    """ Returns True when the layer is a quantized layer.

    Args:
        layer (keras.layers.Layer): layer of interest

    Returns:
        bool: True when the layer is a quantized layer, False otherwise.
    """
    return layer.__class__ in _GLOBAL_LAYER_TO_QLAYER.values()


def _handle_not_quantizable_layers(model):
    """ Checks if the model has not quantizable layers and adds a Dequantizer before.

    Args:
        model (keras.Model): model to check

    Returns:
        keras.Model: the updated model
    """
    def is_quantizable(layer):
        return (get_quantized_layer(layer)
                or is_quantized_layer(layer)
                or layer.__class__ in NO_FLOAT_CUSTOM_QLAYERS)

    # Find layers that cannot be quantized
    for layer in model.layers:
        if not is_quantizable(layer):
            # This layer cannot be quantized, check its inbounds
            inbound = layer.inbound_nodes[0]
            if not inbound.inbound_layers:
                # Skip input layers
                continue
            elif isinstance(inbound.inbound_layers, list):
                raise RuntimeError(f"'{layer.name}' is not quantizable and has multiple inbounds "
                                   "which is not supported.")

            # Check if the layer inbound will be quantized but is not a Dequantizer to prevent
            # adding an additional Dequantizer.
            if (is_quantizable(inbound.inbound_layers) and
                    not isinstance(inbound.inbound_layers, Dequantizer)):
                # Inbound will be quantized, add a Dequantizer after it and return the model
                inbound_name = inbound.inbound_layers.name
                model = insert_layer(model, inbound_name, Dequantizer())
                warnings.warn(f"'{layer.name}' of type {layer.__class__} is not supported to "
                              "quantize, a Dequantizer is added before it and quantization will "
                              "stop at this layer.")
                return model
    return model


def _prepare_output_quantizers(model):
    """ Parse the model and prepare OutputQuantizer configurations for layers requiring them.

    To ensure that an OutputQuantizer will be added to the latest possible layer in a 'block', the
    model is parsed in reverse order. If a layer requires aligned inputs, the function will find the
    preceding layer that can accept an OutputQuantizer and set it in the returned dictionary.

    Args:
        model (keras.Model): the model to parse

    Returns:
        dict: dictionary mapping layer names to an OutputQuantizer config.
    """
    # Dictionary that will contain layers and their OutputQuantizer configurations
    out_quantizer_configs = {}

    # Get quantization parameters
    qparams = get_quantization_params()

    def set_output_quantizer(layer_names, next_layer):
        """ Populates `out_quantizer_configs` with layer names and their OutputQuantizer. """
        for name in layer_names:
            current_layer = model.get_layer(name)
            # Handle special cases were the OutputQuantizer must be per-tensor:
            # - when current_layer has vector outputs,
            # - when next_layer is an Attention layer and the layer is Query or Key
            #   (first and second inputs)
            if isinstance(current_layer, Attention):
                output_shape = current_layer.output_shape[0]
            else:
                output_shape = current_layer.output_shape
            vector_outputs = len(output_shape) < 3
            query_or_key = (isinstance(current_layer, layers.Dense)
                            and isinstance(next_layer, Attention)
                            and next_layer.inbound_nodes[0].inbound_layers.
                            index(current_layer) in [0, 1])
            per_tensor = query_or_key or vector_outputs

            if isinstance(current_layer, layers.ReLU):
                per_tensor = per_tensor or qparams.per_tensor_activations

            # If this is a new entry, set a default configuration
            if name not in out_quantizer_configs:
                axis = "per-tensor" if per_tensor else "per-axis"
                if isinstance(current_layer, layers.ReLU):
                    params = dict(bitwidth=qparams.activation_bits,
                                  signed=qparams.activation_bits >= 8,
                                  axis=axis)
                else:
                    params = dict(bitwidth=qparams.output_bits, axis=axis)
                out_quantizer_configs[name] = dict(output_quantizer=params)

            # If the layer OutputQuantizer configuration is already set, simply check the axis:
            # override the config if the outputs must be per-tensor
            else:
                current_axis = out_quantizer_configs[name]["output_quantizer"]["axis"]
                per_tensor = per_tensor or current_axis == "per-tensor"
                axis = "per-tensor" if per_tensor else "per-axis"
                out_quantizer_configs[name]["output_quantizer"]["axis"] = axis

    def cannot_have_output_quantizer(layer):
        """ Returns True when the layer cannot have an OutputQuantizer. """
        qlayer = get_quantized_layer(layer)
        return (isinstance(layer, Dequantizer)
                or qlayer is None
                or qlayer in _GLOBAL_NO_OUTPUT_QUANTIZER)

    def get_preceding_layer_names(layer):
        """ Retrieve inbounds layers names where an OutputQuantizer can be set. """
        previous_layers = []
        inbounds = layer.inbound_nodes[0].inbound_layers
        if not isinstance(inbounds, list):
            inbounds = [inbounds]
        for inbound in inbounds:
            # Skip input layers
            if isinstance(inbound, layers.InputLayer):
                continue
            # When the given layer cannot have an OutputQuantizer, recursively call the function on
            # this layer
            if cannot_have_output_quantizer(inbound):
                previous_layers.extend(get_preceding_layer_names(inbound))
            else:
                previous_layers.append(inbound.name)
        return previous_layers

    # Parse the layers in reverse order
    for layer in model.layers[::-1]:
        # Find layers that will need aligned inputs
        if get_quantized_layer(layer) in _GLOBAL_ALIGNED_INPUTS:
            # Retrieve the inbounds that can have an OutputQuantizer
            previous_layers = get_preceding_layer_names(layer)
            # Set an OutputQuantizer in their inbounds
            set_output_quantizer(previous_layers, layer)

    return out_quantizer_configs


def quantize_keras(model, q_config=None, qparams=QuantizationParams(), samples=None,
                   num_samples=1024, batch_size=None, epochs=1):
    """Quantizes a Keras model using the provided configuration or parameters.

    Details on how this function behaves:

    - `q_config` has priority over `qparams`, meaning that when a match is found in `q_config` the
      given configuration will be used instead of `qparams`. This is useful to handle specific cases
      (e.g per-tensor output quantizer).
    - when no configuration is given, quantization parameters are deduced from `qparams` and
      OutputQuantizers are automatically set on appropriate layers.
    - `qparams` are only applied to 'float' Keras layers when they are first quantized. As a result,
      when re-quantizing a model, one must provide a complete `q_config`. This is made easy with the
      `dump_config` helper.

    If not already present, a final Dequantizer will be added at the end of the Model.

    The model will also be calibrated using the provided (or randomly generated inputs).

    Args:
        model (keras.Model): the model to quantize
        q_config (dict, optional): quantization configuration as a dictionary mapping layer names to
            their quantization configuration. Defaults to None.
        qparams (QuantizationParams, optional): global quantization parameters. Defaults to
            QuantizationParams().
        samples (tf.Dataset, np.array or generator, optional): calibration samples. When no samples
            are provided, random samples are generated. Defaults to None.
        num_samples (int, optional): number of samples to use in the provided samples or number of
            samples to generate. Defaults to 1024.
        batch_size (int, optional): the batch size. Defaults to None.
        epochs (int, optional): the number of epochs. Defaults to 1.

    Returns:
        keras.Model: the quantized model
    """
    q_config = q_config or dict()

    # Layers will no longer be quantized as soon as a Dequantizer is found
    quantization_stopped = False

    # Handle input_weight_bits using another QuantizationParams where
    # weight_bits = qparams.input_weight_bits, it will be set to False once the input layer has been
    # quantized.
    input_qparams = QuantizationParams(activation_bits=qparams.activation_bits,
                                       per_tensor_activations=qparams.per_tensor_activations,
                                       weight_bits=qparams.input_weight_bits,
                                       output_bits=qparams.output_bits,
                                       buffer_bits=qparams.buffer_bits)

    def _replace_layer(layer):
        nonlocal quantization_stopped, out_quantizer_configs, input_qparams
        config = layer.get_config()

        # Function to handle unsupported arguments in config
        def pop_unsupported_args(class_type):
            for arg, default_value in getattr(class_type, "unsupported_args", {}).items():
                if (arg in config and config[arg] != default_value):
                    raise RuntimeError(
                        f"Argument '{arg}' in layer '{layer.name}' is only "
                        f"supported with default value '{default_value}'. "
                        f"Receives '{config[arg]}'.")
                config.pop(arg, None)

        # Function to handle arguments that should be ignored, i.e. dropped,
        # from config
        def pop_ignored_args(class_type):
            for arg in getattr(class_type, "ignored_args", []):
                config.pop(arg, None)

        # Function that return a quantized layer given its float version
        def get_quantize_layer(layer, quantize_config=None):
            """Quantize float layer in three steps:
                - first, we get its quantized version,
                - second, remove unsupported arguments,
                - then, we return the quantized layer with config updated
            """
            nonlocal quantization_stopped, out_quantizer_configs
            # 1. Check if qlayer exists in custom layers and return the float version of the layer
            # if not
            qlayer = get_quantized_layer(layer)
            if qlayer is None:
                qlayer = layer
                if not (is_quantized_layer(qlayer) or qlayer.__class__ in NO_FLOAT_CUSTOM_QLAYERS):
                    warnings.warn(f"'{ layer.__class__.__name__}' is not supported to quantize. "
                                  "It will be ignored.")
                # If a Dequantizer is found, quantization must be stopped
                quantization_stopped = isinstance(layer, Dequantizer)

            # 2.1 Remove ignored arguments
            pop_ignored_args(qlayer)
            # 2.2 Remove unsupported arguments
            pop_unsupported_args(qlayer)

            # 3. Instantiate quantized layer
            # Instantiate from configuration if there is one
            if quantize_config:
                config['quant_config'] = quantize_config
            # Set the preset default configuration otherwise
            elif layer.name in out_quantizer_configs:
                config['quant_config'] = out_quantizer_configs[layer.name]
            return qlayer.from_config(config)

        # When a not quantizable layer is found, stop quantization returning initial layer
        if quantization_stopped:
            return layer.from_config(config)

        match_conf = q_config.get(layer.name, None)
        try:
            # Overwrite quantization context with input_qparams
            if input_qparams:
                with quantization(input_qparams):
                    qlayer = get_quantize_layer(layer, match_conf)
            else:
                qlayer = get_quantize_layer(layer, match_conf)
        except Exception as e:
            raise type(e)(f"Layer '{layer.name}': {str(e)}") from e
        # When the qlayer is an input layer that has been quantized, disable input_qparams
        input_layers = (QuantizedConv2D, QuantizedDepthwiseConv2D, QuantizedSeparableConv2D,
                        QuantizedDense)
        if input_qparams and isinstance(qlayer, input_layers):
            input_qparams = False
        return qlayer

    # Sanitize the model and make it quantization ready
    model = sanitize(model)

    # Check if the model has not quantizable layers and add a Dequantizer before
    model = _handle_not_quantizable_layers(model)

    # Quantize the model replacing layers with their quantized version
    with quantization(qparams):
        # Determine where to set OutputQuantizers, the return dict will be used as a non-local
        # variable in the _replace_layer function.
        out_quantizer_configs = _prepare_output_quantizers(model)

        new_model = deep_clone_model(model, clone_function=_replace_layer)

    out = new_model.outputs

    # Append Dequantizer at the end of the model to convert the output to float value
    if not isinstance(new_model.layers[-1], Dequantizer) and not quantization_stopped:
        out = Dequantizer()(out)

    # Build the model
    qmodel = Model(new_model.input, out, name=model.name)

    # Now that the model is quantized, proceed to calibration
    calibrate(model, qmodel, samples=samples, num_samples=num_samples, batch_size=batch_size,
              epochs=epochs)
    return qmodel


def quantize(model, q_config=None, qparams=QuantizationParams(), samples=None, num_samples=1024,
             batch_size=None, epochs=1):
    """Quantizes a Keras or ONNX model using the provided configuration or parameters.

    Details on how this function behaves:

    - `q_config` has priority over `qparams`, meaning that when a match is found in `q_config` the
      given configuration will be used instead of `qparams`. This is useful to handle specific cases
      (e.g per-tensor output quantizer). This is only used when quantizing Keras models.
    - when no configuration is given, quantization parameters are deduced from `qparams` and
      OutputQuantizers are automatically set on appropriate layers.
    - `qparams` are only applied to 'float' Keras layers when they are first quantized. As a result,
      when re-quantizing a model, one must provide a complete `q_config`. This is made easy with the
      `dump_config` helper. Note the only configuration supported when quantizing ONNX models is
      8-bit for weights and activations, but per_tensor_activations param will be taken into
      account.

    If not already present, a final Dequantizer will be added at the end of the Model.

    The model will also be calibrated using the provided (or randomly generated inputs).

    Args:
        model (keras.Model or ModelProto): the model to quantize
        q_config (dict, optional): quantization configuration as a dictionary mapping layer names to
            their quantization configuration. Defaults to None.
        qparams (QuantizationParams, optional): global quantization parameters. Defaults to
            QuantizationParams().
        samples (tf.Dataset, np.array or generator, optional): calibration samples. When no samples
            are provided, random samples are generated. Defaults to None.
        num_samples (int, optional): number of samples to use in the provided samples or number of
            samples to generate. Defaults to 1024.
        batch_size (int, optional): the batch size. Defaults to None.
        epochs (int, optional): the number of epochs. This parameter must be 1 for ONNX models.
            Defaults to 1.

    Returns:
        keras.Model or ModelProto: the quantized model
    """
    if type(model) != ModelProto:
        return quantize_keras(model, q_config, qparams, samples, num_samples, batch_size, epochs)
    elif q_config:
        raise ValueError("unsupported parameter q_config for ONNX models quantization")
    elif epochs != 1:
        raise ValueError("unsupported parameter epochs != 1 for ONNX models quantization")
    return quantize_onnx(model, qparams, samples, num_samples, batch_size)


def dump_config(model):
    """Dump the quantization configuration of a quantized model, exporting the configuration for
    each quantized layer.

    Args:
        model (keras.Model): a quantized model.

    Returns:
        dict: the configuration of the model.
    """
    # Get the configuration of the model, iterating over each layer and updating on config.
    config = {}
    for layer in model.layers:
        # Try to take the current quantized configuration
        ly_config = layer.get_config().get('quant_config')

        # Only append quantized configuration
        if is_quantized_layer(layer) and ly_config:
            config[layer.name] = ly_config

    return config
