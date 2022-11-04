from numba import njit
from numpy import exp, power
from constants import z

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
def relu_prime(a):
     return 1 if a > 0 else 0


@njit()
def leaky_relu(a):
    return max(a, z*a)

@njit()
def leaky_relu_prime(a):
    return 1 if a > 0 else z


@njit()
def sigmoid(a):
    return 1.0 / (1.0 + exp(-a))

@njit()
def sigmoid_prime(a):
    sigmoid(a) * (1-sigmoid(a))


@njit()
def tanh(a):
    return (power(exp, 2*a) + 1) / (power(exp, 2*a) - 1)

@njit()
def tanh_prime(a):
    return 1 - power(tanh(z), a)
