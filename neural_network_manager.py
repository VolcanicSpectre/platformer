import numpy as np

from constants import *
from neural_network import NeuralNetwork


class NeuralNetworkManager:
    """Pending Documentation
    """

    def __init__(self, generation_size):
        self.generation_size = generation_size
        generations = [Generation(generation_size) for generation_size in range(NUMBER_OF_GENERATIONS)]


class Generation:
    """Pending Documentation"""

    def __init__(self, size):
        self.size = size
        self.generation = [NeuralNetwork(INITIAL_SIZES) for i in range(self.size)]
        self.innovation_id_matrix = []
        self.current_innovation = 0
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
        child = NeuralNetwork(self)
        for connection1 in parent1.connections:
            for connection2 in parent2.connections:
                if connection1.innovation_id == connection2.innovation_id:
                    if self.rng.integers(0, 1, 1)[0]:
                        child.connections.append(connection1)
                    else:
                        child.connections.append(connection2)


def fitness_function():
    pass
