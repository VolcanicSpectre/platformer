import numba
import numpy as np
from numpy.random import uniform

from node_types import NodeTypes


class NeuralNetwork:
    """Pending Documentation"""

    def __init__(self, generation, sizes):
        self.generation = generation
        self.n_input_nodes, self.n_inital_hidden_nodes, self.n_output_nodes = sizes
        self.node_id_counter = 0
        self.sizes = sizes
        self.nodes = []
        self.connections = []
        self.fitness = 0

    def initialise(self):
        for i in range(self.n_input_nodes):
            pass

        for i in range(self.n_inital_hidden_nodes):
            pass

        for i in range(self.n_output_nodes):
            pass

        for hidden_node in self.nodes[NodeTypes.HIDDEN]:
            pass

    def add_node(self):
        pass

    def add_connection(self):
        pass

    def mutate_weights(self):
        pass

    def load_inputs(self, inputs):
        pass

    def propogate(self):
        pass


class Node:
    def __init__(self, identifier, _type, layer):
        self.id = identifier
        self._type = _type
        self.layer = layer
        self.sum_i = 0
        self.sum_o = 0
        self.connections = []


class Connection:
    def __init__(self, innovation_id, input_node, output_node, weight=uniform(-20, 20, 1)[0],
                 enabled=True, is_recurrent=False):
        self.innovation_id = innovation_id
        self.input_node = input_node
        self.output_node = output_node
        self.weight = weight
        self.enabled = enabled
        self.is_recurrent = is_recurrent


@numba.njit()
def relu(a):
    return np.maximum(0, a)
