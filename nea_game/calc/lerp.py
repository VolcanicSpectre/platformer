def lerp(a: float, b: float, lerp_amount: float) -> float:
    return (a * (1 - lerp_amount)) + (b * lerp_amount)
