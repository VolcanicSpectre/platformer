import numpy as np
from numpy.random import uniform, choice

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
        for node_gene_1 in self.rng.shuffle(self.connection_genes):
            for node_gene_2 in self.rng.shuffle(self.connection_genes):
                if (node_gene_1.id - node_gene_2.id) > 0 or (
                        node_gene_1.type_ == node_gene_2.type_ == NodeTypes.HIDDEN):
                    if not [connection_gene for connection_gene in self.connection_genes if (
                            connection_gene.input_node_id == node_gene_1.id and connection_gene.output_node_id == node_gene_2.id)]:
                        try:
                            innovation_id = self.generation.connections[(node_gene_1.id, node_gene_2.id)]
                        except KeyError:
                            innovation_id = self.generation.current_innovation
                            new_connection_gene = ConnectionGene(innovation_id, nod)


class NodeGene:
    def __init__(self, identifier, type_=NodeTypes.HIDDEN, bias=uniform(-20, 20, 1)[0],
                 activation_function=choice(ACTIVATION_FUNCTIONS)):
        self.identifier = identifier
        self.type_ = type_
        self.bias = bias
        self.input_value = 0
        self.output_value = 0
        self.activation_function = activation_function


class ConnectionGene:
    def __init__(self, innovation_id, input_node_id, output_node_id, weight=uniform(-20, 20, 1)[0], enabled=True):
        self.innovation_id = innovation_id
        self.input_node_id = input_node_id
        self.output_node_id = output_node_id
        self.weight = weight
        self.enabled = enabled


def filter_node_genes(node_gene, node_types):
    return node_gene.type_ in node_types
