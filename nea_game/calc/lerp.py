def lerp(a: float, b: float, lerp_amount: float) -> float:
    """Linearly interpolates between two points.

    Interpolates between the points a and b by the interpolant lerp_amount.
    The parameter lerp_amount is clamped to the range [0, 1].
    This is most commonly used to find a point some fraction of the way along a line between two endpoints

        Args:
            a (float): Endpoint 1
            b (float): Endpoint 2
            lerp_amount (float): The interpolent

        Returns:
            float: The interpolated value
    """
    return (a * (1 - lerp_amount)) + (b * lerp_amount)
