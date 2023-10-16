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
"""
quantizeml main command-line interface.
"""

import argparse
import json
import os
import sys
import re
import numpy as np
import os.path
from onnx import load_model as load_model_onnx, save_model

from .layers import QuantizationParams
from .models import load_model as load_model_keras, quantize, dump_config, check_quantization
from .models.transforms import insert_rescaling


def quantize_model(model_path, quant_config, qparams, samples, num_samples, batch_size, epochs,
                   output_name=None):
    """ CLI entry point to quantize a model using the provided configuration.

    Args:
        model_path (str): Path to the model to quantize.
        quant_config (str): Path to the quantization configuration file.
        qparams (QuantizationParams): global quantization parameters.
        samples (str): calibration samples file path.
        num_samples (int): number of samples to use in the provided samples.
        batch_size (int): batch size for calibration.
        epochs (int): number of epochs for calibration.
        output_name (str, optional): name of the output quantized model. If none provided
            set a default name as <model>_<config>.h5. Defaults to None.
    """
    # Build name for the output model
    model_name = os.path.splitext(model_path)[0]
    _, ext = os.path.splitext(model_path)
    model_ext = ext.lower()

    # Set default output_name using the config when there is one and the qparams otherwise
    if output_name is None:
        if quant_config:
            output_name = f"{model_name}_{os.path.splitext(os.path.basename(quant_config))[0]}.h5"
        else:
            # Quantization suffix has a well-identified structure, only keep the actual base name
            # without it
            model_name = re.split(r'(_i\d_w\d_a\d)', model_name)[0]
            output_name = f"{model_name}_i{qparams.input_weight_bits}_w{qparams.weight_bits}"\
                          f"_a{qparams.activation_bits}{model_ext}"

    # Load the configuration file
    if quant_config:
        with open(quant_config) as f:
            config = json.load(f)
    else:
        config = None

    # Load the model
    if model_ext == ".h5":
        model = load_model_keras(model_path)
    else:
        model = load_model_onnx(model_path)

    # Load calibration samples
    if samples:
        data = np.load(samples)
        samples_arr = np.concatenate([data[item] for item in data.files])
        num_samples = len(samples_arr)
    else:
        samples_arr = None

    # Quantize the model and save it
    print(f"Quantizing model {model_path} with configuration file {quant_config}.")
    model_q = quantize(model, q_config=config, qparams=qparams, samples=samples_arr,
                       num_samples=num_samples, batch_size=batch_size, epochs=epochs)
    if model_ext == ".h5":
        model_q.save(output_name, include_optimizer=False)
    else:
        save_model(model_q, output_name)
    print(f"Saved quantized model to {output_name}.")


def dump_model_config(model_path, output_name=None):
    """ CLI entry point to dump the quantization configuration from a model.

    Args:
        model_path (str): Path to the model to extract the configuration from.
        output_name (str): Path to save the configuration.
            Defaults to <model_path>_quant_config.json.
    """
    # Build name for the output model
    if output_name is None:
        model_name = os.path.splitext(model_path)[0]
        output_name = f"{model_name}_quant_config.json"

    # Load the model and get its quantization configuration
    model = load_model_keras(model_path)
    config = dump_config(model)
    with open(output_name, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Saved quantization configuration to {output_name}.")


def check_quantized_model(model_path):
    """ CLI entry point to check model quantization.

    Args:
        model_path (str): Path to the model on which apply the weights.
    """
    model = load_model_keras(model_path)
    messages = check_quantization(model)
    for msg in messages:
        print(msg)


def insert_rescaling_and_save(model_path, dest_path, scale, offset):
    """ CLI entry point to insert a Rescaling layer in a model.

    Args:
        model_path (str): Path to the source model.
        dest_path (str): Path to the destination model.
        scale (float): the Rescaling scale
        offset (float): the Rescaling offset
    """
    model = load_model_keras(model_path)
    updated = insert_rescaling(model, scale, offset)
    updated.save(dest_path)


def main():
    """ CLI entry point.

    Contains an argument parser with specific arguments depending on the model to be created.
    Complete arguments lists available using the -h or --help argument.

    """
    # Define a strictly positive int type for parameters
    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("%s is an invalid value, must be >0." % value)
        return ivalue

    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="action")
    sp.add_parser("version", help="Display quantizeml version.")

    # Quantize arguments
    q_parser = sp.add_parser(
        "quantize", help="Quantize an input model, given a quantization configuration file.")
    q_parser.add_argument("-m", "--model", type=str, required=True, help="Model to quantize")
    q_parser.add_argument("-c", "--quantization_config", type=str, default=None,
                          help="Quantization configuration file")
    q_parser.add_argument("-a", "--activation_bits", type=positive_int, default=8,
                          help="Activation quantization bitwidth")
    q_parser.add_argument("--per_tensor_activations", action='store_true',
                          help="Quantize activations per-tensor")
    q_parser.add_argument("-w", "--weight_bits", type=positive_int, default=8,
                          help="Weight quantization bitwidth")
    q_parser.add_argument("-i", "--input_weight_bits", type=positive_int, default=8,
                          help="Input layer weight quantization bitwidth")
    q_parser.add_argument("-b", "--buffer_bits", type=positive_int, default=32,
                          help="Buffer quantization bitwidth")
    q_parser.add_argument("-s", "--save_name", type=str,
                          help="Name for saving the quantized model.")
    q_parser.add_argument("-sa", "--samples", type=str, default=None,
                          help="Set of samples to calibrate the model (.npz file).")
    q_parser.add_argument("-ns", "--num_samples", type=positive_int, default=1024,
                          help="Number of samples to use for calibration, only used when 'samples'"
                               " is not provided.")
    q_parser.add_argument("-bs", "--batch_size", type=positive_int, default=32,
                          help="Batch size for calibration.")
    q_parser.add_argument("-e", "--epochs", type=positive_int, default=1,
                          help="Number of epochs for calibration.")

    # Dump config arguments
    c_parser = sp.add_parser(
        "config", help="Extract quantization configuration from a Keras model.")
    c_parser.add_argument("-m", "--model", type=str, required=True,
                          help="Model to extract config from.")
    c_parser.add_argument("-o", "--output_path", type=str, help="Store quantization configuration. "
                          "Defaults to <model>_quant_config.json")

    # Check action and arguments
    c_parser = sp.add_parser(
        "check", help="Check the quantization of a Keras model to detect issues that can be fixed "
        "by adjusting the quantization configuration.")
    c_parser.add_argument("-m", "--model", type=str, required=True, help="Model to check")

    # insert_rescaling action and arguments
    ir_parser = sp.add_parser(
        "insert_rescaling", help="Insert a Rescaling layer at the beginning of the Keras model.")
    ir_parser.add_argument("-m", "--model", type=str, required=True,
                           help="Path to the source Model")
    ir_parser.add_argument("-d", "--dest_model", type=str, required=True,
                           help="Path to the destination Model")
    ir_parser.add_argument("-s", "--scale", type=float, required=True,
                           help="The Rescaling scale")
    ir_parser.add_argument("-o", "--offset", type=float, required=True,
                           help="The Rescaling offset")

    args = parser.parse_args()

    if args.action == "version":
        # importlib.metadata was introduced in Python 3.8 and is available to older versions as the
        # importlib-metadata project
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata
        print(metadata.version('quantizeml'))
    elif args.action == "quantize":
        qparams = QuantizationParams(activation_bits=args.activation_bits,
                                     per_tensor_activations=args.per_tensor_activations,
                                     weight_bits=args.weight_bits,
                                     input_weight_bits=args.input_weight_bits,
                                     buffer_bits=args.buffer_bits)
        quantize_model(
            model_path=args.model,
            quant_config=args.quantization_config,
            qparams=qparams,
            samples=args.samples,
            num_samples=args.num_samples,
            batch_size=args.batch_size,
            epochs=args.epochs,
            output_name=args.save_name
        )
    elif args.action == "config":
        dump_model_config(
            model_path=args.model,
            output_name=args.output_path,
        )
    elif args.action == "check":
        check_quantized_model(args.model)
    elif args.action == "insert_rescaling":
        insert_rescaling_and_save(args.model, args.dest_model, args.scale, args.offset)
