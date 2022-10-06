import numpy as np
import numba
from time import perf_counter


class NeuralNetwork:
    """Pending Documentation"""

    def __init__(self, sizes):
        self.n_layers = len(sizes)
        self.sizes = sizes
        self.node_genes =

        self.connection_genes = np.array()

    def add_node(self):
        pass

    def add_connection(self):
        pass


@numba.njit()
def relu(a):
    return np.maximum(0, a)
