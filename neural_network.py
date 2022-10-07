import numpy as np
import numba
from time import perf_counter
from node_types import INPUT, HIDDEN, OUTPUT
from numpy.random import default_rng

class NeuralNetwork:
    """Pending Documentation"""

    def __init__(self, sizes):
        self.n_input_nodes, self.n_inital_hidden_nodes, n_output_nodes = sizes
        self.node_id_counter = 0
        self.sizes = sizes
        self.nodes = {INPUT: [],  HIDDEN: [], OUTPUT: []}
        
    def initialise(self):
        for i in range(self.n_input_nodes):
            self.add_node(0, _type=INPUT)

        for i in range(self.n_inital_hidden_nodes):
            self.add_node(1, _type=HIDDEN)

        for i in range(self.n_output_nodes):
            self.add_node(2, _type=OUTPUT)

        
        for hidden_node in self.nodes[HIDDEN]:
            for input_node in self.nodes[INPUT]:
                self.add_connection(input_node, hidden_node)
            for output_node in self.nodes[OUTPUT]:
                self.add_connection(hidden_node, output_node)
                
            

    def add_node(self, layer, _type=HIDDEN):
        self.nodes.append(Node(self.node_id_counter, _type, layer))
        self.node_id_counter += 1

    def add_connection(self, current_node, target_node):
        self.current_node.connections.append(Connection(innovation_id=0, current_node=current_node, target_node=target_node))
    
    def mutate_weights(self):
        pass

    def load_inputs(self, inputs):
        for input_node, input_value in zip(self.nodes["inputs"], inputs):
            input_node.sum_o = input_value
    
    def propogate(self, layer):
        for node in self.nodes["hidden"]:
            if node.layer == layer:
                pass


    
class Node:
    def __init__(self, identifier, _type , layer):
        self.id = id
        self._type = _type
        self.layer = layer
        self.sum_i = 0
        self.sum_o = 0
        self.connections = []

class Connection:
    def __init__(self, innovation_id, input_node, output_node, weight=default_rng.integers(low=-20, high=20, size=1)[0], enabled=True, is_recurrent=False):
        self.innovation_id = innovation_id
        self.input_node = input_node
        self.output_node = output_node
        self.weight = weight
        self.enabled = enabled
        self.is_recurrent = is_recurrent


@numba.njit()
def relu(a):
    return np.maximum(0, a)
