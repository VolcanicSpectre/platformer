import numpy as np
import numba
from time import perf_counter


class NeuralNetwork:
    """Pending Documentation"""

    def __init__(self, sizes):
        self.n_layers = len(sizes)
        self.sizes = sizes
        self.nodes = {"input": [],  "hidden": [], "output": []}

        self.something = {}


    def add_node(self):
        pass

    def add_connection(self):
        pass
    
    def mutate_weights(self):
        pass

    def load_inputs(self, inputs):
        for input_node, input_value in zip(self.nodes["inputs"], inputs):
            input_node.sum_o = input_value
    
    def propogate(self, layer):
        for node in self.nodes["hidden"]:
            if node.layer == layer:
                


    

class Node:
    def __init__(self, identifier, _type , layer):
        self.id = id
        self._type = _type
        self.layer = layer
        self.sum_i = 0
        self.sum_o = 0

class Connection:
    def __init__(self, innovation_id, i_node_id, o_node_id, weight, enabled=True, is_recurrent=False):
        self.innovation_id = innovation_id
        self.i_node_id = i_node_id
        self.o_node_id = o_node_id
        self.weight = weight
        self.enabled = enabled
        self.is_recurrent = is_recurrent


@numba.njit()
def relu(a):
    return np.maximum(0, a)
