from constants import *
from neural_network import NeuralNetwork


class NeuralNetworkManager:
    def __init__(self, population_size):
        self.population_size = population_size
        generations = [Generation(population_size) for i in range(NUMBER_OF_GENERATIONS)]



class Generation:
    def __init__(self, population_size):
        self.generation = [NeuralNetwork(INITIAL_SIZES) for i in range(population_size)]

    def __iter__(self):
        return iter(self.generation)

    def selection(self):
        [fitness_function(nn) for nn in self]

            




def fitness_function():
    pass