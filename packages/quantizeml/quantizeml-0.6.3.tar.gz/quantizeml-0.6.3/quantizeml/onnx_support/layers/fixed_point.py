import numpy as np


def to_fixed_point(x, bitwidth, signed=True):
    """Convert a number to a FixedPoint representation

    The representation is composed of a mantissa and an implicit exponent expressed as
    a number of fractional bits, so that:

    x ~= mantissa . 2 ** -frac_bits

    The mantissa is an integer whose bitwidth and signedness are specified as parameters.

    Args:
        x (np.ndarray): the source number or array
        bitwidth (np.ndarray): the desired bitwidth
        signed (bool, optional): when reserving a bit for the sign. Defaults to True.

    Returns:
        np.ndarray, np.ndarray: the mantissa and fractional bits
    """
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    # Evaluate the number of bits available for the mantissa
    mantissa_bits = bitwidth - 1 if signed else bitwidth
    # Evaluate the number of bits required to represent the whole part of x
    # as the power of two enclosing the absolute value of x
    # Note that it can be negative if x < 0.5
    y = np.abs(x)
    whole_bits = np.ceil(np.log2(y)).astype(np.int32)
    # Force whole_bits = 0 when x is 0
    whole_bits = np.where(y == 0, 0, whole_bits)
    # Deduce the number of bits required for the fractional part of x
    # Note that it can be negative if the whole part exceeds the mantissa
    frac_bits = mantissa_bits - whole_bits
    # Evaluate the 'scale', which is the smallest value that can be represented (as 1)
    scale = 2. ** -frac_bits
    # Evaluate the minimum and maximum values for the mantissa
    mantissa_min = -2 ** mantissa_bits if signed else 0
    mantissa_max = 2 ** mantissa_bits - 1
    # Evaluate the mantissa by quantizing x with the scale, clipping to the min and max
    mantissa = np.clip(np.round(x / scale), mantissa_min, mantissa_max).astype(np.int32)
    return mantissa, frac_bits


def to_float(mantissa, frac_bits):
    return mantissa * 2. ** -frac_bits
