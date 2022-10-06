import numpy as np
import numba


class NeuralNetwork:
    def __init__(self, sizes):
        self.n_layers = len(sizes)
        self.sizes = sizes
        self.initialise_default_weights_and_biases()

    def initialise_default_weights_and_biases(self):
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]
        self.weights = [np.random.randn(y, x) / np.sqrt(x)
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

    def feed_forward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = relu(np.dot(w, a) + b)
        return a

    def add_node(self):
        pass

    def add_connection(self):
        pass


@numba.njit()
def relu(a):
    return np.maximum(0, a)
