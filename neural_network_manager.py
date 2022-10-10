import numpy as np
from constants import *
from neural_network import NeuralNetwork


class Generation:
    """Pending Documentation"""

    def __init__(self, size):
        self.size = size
        self.generation = [NeuralNetwork(INITIAL_SIZES) for i in range(self.size)]
        self.connections = {}
        self.current_innovation = 0
        self.distance_threshold = 4
        self.desired_number_of_species = 5
        self.rng = np.random.default_rng()

    def __iter__(self):
        return iter(self.generation)

    def __getitem__(self, index):
        return self.generation[index]

    def selection(self):
        mating_pool = []
        chromosome_fitness_values = np.array([nn for nn in self])
        total_population_fitness = np.sum(chromosome_fitness_values)

        chromosome_selection_probability = np.array(
            [(chromosome_fitness_value / total_population_fitness) for chromosome_fitness_value in
             chromosome_fitness_values], dtype=np.float64)

        chromosome_cumulative_probabilty = [np.sum(chromosome_selection_probability[:index]) for
                                            index, chromosome_probabilty in enumerate(chromosome_selection_probability)]

        for nn, index, cumulative_chromosome_probability in zip(self, enumerate(chromosome_cumulative_probabilty)):
            rn = self.rng.random()
            if rn <= cumulative_chromosome_probability:
                mating_pool.append(nn)
            elif chromosome_cumulative_probabilty[index - 1] < rn <= cumulative_chromosome_probability:
                mating_pool.append(self[self.rng.integers(low=2, high=self.size, size=1)[0]])

        return mating_pool

    def reproduction(self, mating_pool):
        pass

    def crossover(self, parent1, parent2):
        pass

    def get_excess_and_disjoint_connection_genes(self, genome1, genome2):
        excess_and_disjoint_connection_genes = []

    def get_average_enabled_weight_difference(self, genome1, genome2):
        innovation_ids_of_shared_connections = [connection_gene_1.innovation_id for connection_gene_1 in
                                                genome1.connection_genes for connection_gene_2 in
                                                genome2.connection_genes if
                                                connection_gene_1.innovation_id == connection_gene_2.innovation_id]

    def get_distance_between_2_genomes(self, genome1, genome2):
        return self.get_excess_and_disjoint_genes(genome1, genome2) + self.get_average_enabled_weight_difference(
            genome1, genome2)


def fitness_function():
    pass
