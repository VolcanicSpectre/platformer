import numpy as np
from numpy.random import uniform, choice
from functools import lru_cache

from constants import *
from node_types import NodeTypes


class Genome:
    def __init__(self, generation):
        self.generation = generation
        self.rng = np.default_rng()
        self.node_genes = []
        self.connection_genes = []

    def feed_forward(self, inputs):
        for input_node, input_value in zip(
                [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.INPUT], inputs):
            input_node.output_value = input_value

        for node_gene in [node_gene for node_gene in self.node_genes if node_gene.type_ != NodeTypes.INPUT]:
            for connection in [connection for connection in self.connection_genes if
                               (connection.enabled and connection.output_id == node_gene.identifier)]:
                node_gene.input_value += self.node_genes[connection.input_node_id].output_value * connection.weight
            node_gene.output_value = node_gene.activation_function(node_gene.output_value)

        outputs = [node_gene.output_value for node_gene in self.node_genes if node_gene.type == NodeTypes.OUTPUT]

        for node_gene in self.node_genes:
            node_gene.input_value, node_gene.output_value = 0, 0

        return outputs

    def mutate_weights(self):
        for connection_gene in self.connection_genes:
            seed = self.rng.random_sample()
            if seed < COMPLETY_MUTATE_WEIGHT:
                connection_gene.weight = (self.rng.random_sample - 0.5) * 2
            else:
                connection_gene.weight += self.rng.random_sample() * VARIANCE_FOR_WEIGHT_MUTATION_MULTIPLIER

    def mutate_add_connection(self):
        for i in range(20):
            node_gene_1, node_gene_2 = [choice(self.node_genes, 1)[0] for i in range(2)]
            if self.valid_node_pair(node_gene_1, node_gene_2):
                self.connection_genes.append(ConnectionGene(None, node_gene_1, node_gene_2))

    def valid_node_pair(self, node_gene_1, node_gene_2):
        if [connection_gene for connection_gene in self.connection_genes if
            (connection_gene.input_node_id == node_gene_1.id and connection_gene.output_node_id == node_gene_2.id)]:
            return False
        if node_gene_1.id == node_gene_2.id:
            return False
        if node_gene_1.layer == node_gene_2.layer:
            return False
        if node_gene_1.layer > node_gene_2.layer and not ALLOW_RECURRENT_CONNECTIONS:
            return False

        return True

    def mutate_add_node(self):
        connection_for_new_node = \
            choice([connection_gene for connection_gene in self.connection_genes if not connection_gene.recurrent])[0]

        connection_for_new_node.enabled = False
        new_node_gene = NodeGene(len(self.node_genes), layer=connection_for_new_node.input_node + 1)
        new_connection_gene_1 = ConnectionGene(None, connection_for_new_node.input_node_id, new_node_gene.identifier)
        new_connection_gene_2 = ConnectionGene(None, new_node_gene.identifier, connection_for_new_node.output_node_id)
        self.connection_genes.append(new_connection_gene_1)
        self.connection_genes.append(new_connection_gene_2)

    def set_node_layers(self):
        for hidden_node_gene in [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.HIDDEN]:


    @lru_cache(10)
    def get_longest_path_to_input_layer(self, node_gene):
        path_lengths = []
        for connection_termianting_at_node in [connection_gene for connection_gene in self.connection_genes if connection_gene.output_node_id == node_gene.output_node_id]
            if self.node_genes[connection_termianting_at_node.input_node_id].type_ == NodeTypes.INPUT:
                return 1
            else:
                return self.get_longest_path_to_input_layer()

class NodeGene:
    def __init__(self, identifier, layer, type_=NodeTypes.HIDDEN, bias=uniform(-20, 20, 1)[0],
                 activation_function=choice(ACTIVATION_FUNCTIONS, 1)[0]):
        self.identifier = identifier
        self.layer = layer
        self.type_ = type_
        self.bias = bias
        self.input_value = 0
        self.output_value = 0
        self.activation_function = activation_function


class ConnectionGene:
    def __init__(self, innovation_id, input_node_id, output_node_id, weight=uniform(-20, 20, 1)[0], enabled=True,
                 recurrent=False):
        self.innovation_id = innovation_id
        self.input_node_id = input_node_id
        self.output_node_id = output_node_id
        self.weight = weight
        self.enabled = enabled
        self.recurrent = recurrent


def filter_node_genes(node_gene, node_types):
    return node_gene.type_ in node_types
