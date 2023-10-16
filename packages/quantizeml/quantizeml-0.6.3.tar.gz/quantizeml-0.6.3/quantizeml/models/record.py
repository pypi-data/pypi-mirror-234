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
Recording utilities.
"""

__all__ = ["record_quantization_variables"]

import numpy as np

from quantizeml.layers.buffer_temp_conv import reset_buffers
from ..layers import recording


def record_quantization_variables(model):
    """Helper method to record quantization objects in the graph.

    Passing a dummy sample through the model in recording mode, this triggers the
    recording of all dynamic quantization objects.

    Args:
        model (keras.Model): model for which objects need to be recorded.
    """
    def _gen_dummy_sample(shape):
        sample = np.random.randint(0, 255, size=(1, *shape))
        return sample.astype(np.float32)
    # Reset FIFO buffers to allow inference
    reset_buffers(model)
    with recording(True):
        # Create sample and pass it through the model to calibrate variables
        sample = _gen_dummy_sample(model.input.shape[1:])
        model(sample)
