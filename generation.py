from numpy.random import default_rng
import matplotlib.pyplot as plt
from constants import *
from genome import Genome, load_genome
from math import inf
import sys
import pygame


class Population:
    """Pending Documentation"""

    def __init__(self, generation_number, distance_threshold):
        self.generation_number = generation_number
        self.generation = []
        self.connections = {}
        self.current_innovation = 0
        self.distance_threshold = distance_threshold
        self.rng = default_rng()

    def initilaise(self):
        self.generation = [Genome(self, blank_initialise=False) for i in range(GENERATION_SIZE)]

    def advance_generation(self):
        total_fitness = 0
        for genome in self.generation:
            genome.mutate()

        for genome in self.generation:
            genome.list_of_outputs = []
            for input_value in INPUTS:
                genome.feed_forward(input_value)

        for genome in self.generation:
            genome.fitness = fitness_function(genome)
            total_fitness += genome.fitness
            if genome.fitness > 3.95:
                print("FITNESS THRESHOLD REACHED")
                genome.save_genome()
                sys.exit()

        print(f"GEN {self.generation_number}")
        print(f"AVERAGE FITNESS: {total_fitness / 100}")

        species = self.speciation()
        print(len(species.keys()))
        print("\n\n")

        number_of_offspring = GENERATION_SIZE
        population_average_adjusted_fitness = sum(
            [calulate_total_adjusted_fitness(species[species_number]) for species_number in species]) / len(
            self.generation)

        number_of_offspring = GENERATION_SIZE

        new_generation = []

        for species_number in species:
            allowed_number_of_offspring = min(round((calulate_total_adjusted_fitness(species[species_number]) * len(
                species[species_number]) / population_average_adjusted_fitness)), number_of_offspring)
            number_of_offspring -= allowed_number_of_offspring
            for i in range(allowed_number_of_offspring):
                mating_pool = self.roulette_wheel_selection(species[species_number])
                new_generation.append(self.crossover(mating_pool))

        self.generation_number += 1
        self.generation = new_generation

    def speciation(self):
        current_species_number = 0
        genomes = self.generation[:]
        species = {}
        while genomes:
            current_species_number += 1
            random_genome = self.rng.choice(genomes, 1)[0]
            genomes.remove(random_genome)
            species[current_species_number] = [random_genome]
            for genome in genomes[:]:
                if self.get_distance_between_2_genomes(random_genome, genome) < self.distance_threshold:
                    species[current_species_number].append(genome)
                    genomes.remove(genome)

        if len(species.keys()) < TARGET_NUMBER_OF_SPECIES:
            self.distance_threshold += DISTANCE_THRESHOLD_STEP
        elif len(species.keys()) > TARGET_NUMBER_OF_SPECIES:
            self.distance_threshold -= DISTANCE_THRESHOLD_STEP

        return species

    def roulette_wheel_selection(self, genomes, mating_pool_size=2):
        mating_pool = []
        total_species_fitness = sum([genome.fitness for genome in genomes])
        max_percent_genomes = sorted(genomes)

        max_percent_genome_fitness_values = sorted([genome.fitness for genome in genomes])
        total_max_percent_species_fitness = sum(max_percent_genome_fitness_values)

        genome_selection_probability = [(genome_fitness_value / total_max_percent_species_fitness) for
                                        genome_fitness_value in max_percent_genome_fitness_values]
        return self.rng.choice(max_percent_genomes, p=genome_selection_probability, size=mating_pool_size)

    def crossover(self, parents):
        parent1, parent2 = parents

        fittest_parent = max(parent1, parent2)
        child = copy_genome(fittest_parent)
        shared_connections = get_shared_connections(parent1, parent2)
        weights_of_shared_connections = get_weights_of_shared_connections(parent1, parent2)
        for connection_gene in child.connection_genes:
            for index, shared_connection_gene in enumerate(shared_connections):
                if connection_gene.innovation_id == shared_connection_gene.innovation_id:
                    connection_gene.weight = self.rng.choice(weights_of_shared_connections[index], 1)[0]

        return child

    def get_excess_and_disjoint_connection_genes(genome1, genome2):
        genome1.connection_genes.sort(key=lambda connection_gene: connection_gene.innovation_id)
        genome2.connection_genes.sort(key=lambda connection_gene: connection_gene.innovation_id)

        genome_1_excess_and_disjoint_connection_genes = []
        genome_2_excess_and_disjoint_connection_genes = []
        disjoint_connection_genes = []
        excess_connection_genes = []

        genome_1_maximum_innovation_id = max(
            [connection_gene.innovation_id for connection_gene in genome1.connection_genes]),
        genome_2_maximum_innovation_id = max(
            [connection_gene.innovation_id for connection_gene in genome2.connection_genes])

        for connection_gene_1 in genome1.connection_genes:
            if connection_gene_1.innovation_id not in [connection_gene_2.innovation_id for connection_gene_2 in
                                                       genome2.connection_genes]:
                genome_1_excess_and_disjoint_connection_genes.append(connection_gene_1)

        for connection_gene_2 in genome2.connection_genes:
            if connection_gene_2.innovation_id not in [connection_gene_1.innovation_id for connection_gene_1 in
                                                       genome1.connection_genes]:
                genome_2_excess_and_disjoint_connection_genes.append(connection_gene_2)

        for connection_gene_1 in genome_1_excess_and_disjoint_connection_genes:
            if connection_gene_1.innovation_id > genome_2_maximum_innovation_id:
                excess_connection_genes.append(connection_gene_1)
        for connection_gene_2 in genome_2_excess_and_disjoint_connection_genes:
            if connection_gene_2.innovation_id > genome_1_maximum_innovation_id:
                excess_connection_genes.append(connection_gene_2)

    def get_number_of_excess_and_disjoint_connection_genes(self, genome1, genome2):
        # Will need to be able to get the exxcess and disjoint connections later
        number_of_excess_and_disjoint_connection_genes = 0
        for connection_gene_1 in genome1.connection_genes:
            if connection_gene_1.innovation_id not in [connection_gene_2.innovation_id for connection_gene_2 in
                                                       genome2.connection_genes if
                                                       connection_gene_2.enabled] and connection_gene_1.enabled:
                number_of_excess_and_disjoint_connection_genes += 1

        for connection_gene_2 in genome2.connection_genes:
            if connection_gene_2.innovation_id not in [connection_gene_1.innovation_id for connection_gene_1 in
                                                       genome1.connection_genes if
                                                       connection_gene_1.enabled] and connection_gene_2.enabled:
                number_of_excess_and_disjoint_connection_genes += 1

        return number_of_excess_and_disjoint_connection_genes

    def get_distance_between_2_genomes(self, genome1, genome2):
        # Could Normalise the Number of Excess and Disjoint Connections by N
        return self.get_number_of_excess_and_disjoint_connection_genes(genome1,
                                                                       genome2) + get_average_enabled_weight_difference(
            genome1, genome2)


def copy_genome(genome):
    copied_genome = Genome(genome.generation)
    copied_genome.node_genes = genome.node_genes.copy()
    copied_genome.connection_genes = genome.connection_genes.copy()
    return copied_genome


def get_weights_of_shared_connections(genome1, genome2):
    return [(connection_gene_1.weight, connection_gene_2.weight) for connection_gene_1, connection_gene_2 in
            zip(genome1.connection_genes, genome2.connection_genes) if
            connection_gene_1.innovation_id == connection_gene_2.innovation_id]


def get_shared_connections(genome1, genome2):
    return [connection_gene_1 for connection_gene_1, connection_gene_2 in
            zip(genome1.connection_genes, genome2.connection_genes) if
            connection_gene_1.innovation_id == connection_gene_2.innovation_id]


def get_average_enabled_weight_difference(genome1, genome2):
    weights_of_shared_connections = get_weights_of_shared_connections(genome1, genome2)
    if weights_of_shared_connections:
        return sum(abs(weight_1 - weight_2) for weight_1, weight_2 in weights_of_shared_connections) / len(
            weights_of_shared_connections)
    else:
        return inf


def calulate_total_adjusted_fitness(genomes):
    return sum([genome.fitness / len(genomes) for genome in genomes])


def fitness_function(genome):
    fitness = 4
    for output, expected_output in zip(genome.list_of_outputs, EXPECTED_OUTPUTS):
        fitness -= (output - expected_output) ** 2

    return fitness


if __name__ == "__main__":
    population = Population(0, 2)
    population.initilaise()
    running = True
    while running:
        population.advance_generation()

    genome = load_genome("80_21.pickle")

    for input_value, output_value in zip(INPUTS, genome.list_of_outputs):
        print(f"{input_value} -> {output_value}")

    print(genome.fitness)
    width, height = 1920, 1080

    screen = pygame.display.set_mode((width, height))
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        genome.draw(screen)
        pygame.display.update()
