"""Returns the sign of flt. Return value is 1 when flt is positive or zero, -1 when flt is negative.
"""


def sign(flt: float) -> float:
    """Returns the sign of flt.
        Return value is 1 when flt is positive or zero, -1 when flt is negative.


    Args:
        flt (float): The value to determine the sign of

    Returns:
        float: The sign of flt
    """
    return 1 if flt >= 0 else -1
