import numpy as np
import numba
from time import perf_counter


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
            a = reluv(np.dot(w, a) + b)
        return a

    def add_node(self):
        pass

    def add_connection(self):
        pass


@numba.vectorize([numba.float64(numba.float64)])
def reluv(a):
    return np.maximum(0, a)


if __name__ == "__main__":
    s = [720, 500, 300, 4]
    nn = NeuralNetwork(s)
    print("done")

    N = 1000

    a = [np.random.random_sample() for x in range(720)]

    v1 = perf_counter()
    for i in range(N):
        o = nn.feed_forward(a)

    print(f"vectorize: {(perf_counter() - v1) / N}")
