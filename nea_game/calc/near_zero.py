"""Defines a thresholod and a funtion to approximate floats close to zero
"""
from math import isclose
from functools import partial

THRESHOLD = 1e-5
is_close_to_zero = partial(isclose, b=0, abs_tol=THRESHOLD)


def near_zero(flt: float) -> float:
    """If a float is close to zero then zero is returned othewise the flaot itself is returned

    Args:
        flt (float): The float to be approximated

    Returns:
        float: The approximated value of the float
    """
    if is_close_to_zero(flt):
        return 0
    return flt
