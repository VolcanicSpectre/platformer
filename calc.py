from numba import njit
from numpy import exp, power, zeros, flipud, fliplr
from numba import guvectorize, int64, float64
from constants import *


def move_towards(current, target, max_delta):
    """Returns the value closest to the target value with a maximimm change of max_delta"""
    if current > target:
        return max(current - max_delta, target)
    else:
        return min(current + max_delta, target)

def convolve2d(image, kernel, stride, output_shape, crosscorrelate=True):
    if crosscorrelate:
        kernel = flipud(fliplr(kernel))
    kernel_size = kernel.shape[0]
    
    output = zeros(output_shape) 
    for y in range(image.shape[1]):
        if y > image.shape[1] - kernel_size:
            break
        
        if y % stride == 0:
            for x in range(image.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - kernel_size:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        output[x, y] = (kernel * image[x: x + kernel_size, y: y + kernel_size]).sum()
                except:
                    break

    return output


def get_mean_squared_error(predicted, labels):
    mse = np.sum((predicted - labels)**2)
    derivative = 2 * (predicted - labels)

    return mse, derivative

@njit()
def relu(a):
    return max(0, a)

@njit()
def relu_prime(a):
     return 1 if a > 0 else 0



def leaky_relu(a):
    return max(a, z*a)


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
