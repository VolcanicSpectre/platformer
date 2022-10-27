from numba import njit
from numpy import exp
from math import pow

def move_towards(current, target, max_delta):
    """Returns the value closest to the target value with a maximimm change of max_delta"""
    if current > target:
        return max(current - max_delta, target)
    else:
        return min(current + max_delta, target)


@njit()
def relu(a):
    return max(0, a)


@njit()
def sigmoid(a):
    return 1.0 / (1.0 + exp(-a))


@njit()
def tanh(a):
    return (pow(exp, 2*a) + 1) / (pow(exp, 2*a) - 1)

