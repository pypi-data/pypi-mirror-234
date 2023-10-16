import numpy as np

# Akida weights range is [-127, 127], int8
AKIDA_W_MAX = 127.0


def quantize_value_shift(x, scale, bitwidth=8, signed=True):
    # Decrease bitwidth when signed
    if signed:
        bitwidth -= 1
    # Project input
    proj_x = x * scale
    # Inputs needs to be quantized to bitwidth-bit
    epsilon = 2**-8
    x_int_bits = np.ceil(np.log2(np.abs(proj_x + epsilon)))
    qx_shift = np.maximum(0, x_int_bits - bitwidth).astype(np.int32)
    qx_8 = np.round(proj_x / (2 ** qx_shift)).astype(np.int32)
    # Rebuild quantized inputs
    return qx_8 << qx_shift


def quantize_weights(kernel, bias, zero_point=0):
    """Quantize weights and bias to Akida-compatible format.

    Args:
        kernel: 2D weights tensor
        bias: 1D bias tensor
        zero_point: 1D integer tensor to fold in bias. Defaults to 0.

    Returns:
        qkernel: quantized kernel
        qbias: quantized bias
        scale: scale factor to convert float to quantized int
    """
    q_axis = tuple(range(1, kernel.ndim))
    # Absolute max value calculated on first dim
    abs_max = np.abs(kernel).max(q_axis)
    # Clip absolute max value
    abs_max = np.maximum(abs_max, 2.**-16)
    # Calculate float scale
    scale = AKIDA_W_MAX / abs_max
    # Reshape scale to broadcast it from the first dimension
    k_scale = np.expand_dims(scale, axis=q_axis)
    # Project weights and bias to quantized int8 domain, but keeping them in
    # float
    proj_kernel = kernel * k_scale
    # Now kernel can be finally be quantized to int8
    qkernel = np.round(proj_kernel)
    qkernel = np.clip(qkernel, -128, 127)
    qkernel = qkernel.astype(np.int8)

    # Fold zero point into bias previous to quantize it.
    # Note this is possible if we project each zero point through
    # its respective axis in the weights (with FCXY format)
    align_shape = [1] * (kernel.ndim - 2)
    zero_point = np.reshape(zero_point, (-1, *align_shape))
    bias = bias - ((zero_point.astype("int32") * qkernel).sum(axis=q_axis) / scale)

    # Quantize bias
    qbias = quantize_value_shift(bias, scale)
    return qkernel, qbias, scale
