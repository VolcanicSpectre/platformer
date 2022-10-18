from numpy.random import default_rng
from itertools import repeat
from constants import *
from genome import Genome


class Generation:
    """Pending Documentation"""

    def __init__(self, size, distance_threshold):
        self.generation = []
        self.connections = {}
        self.current_innovation = 0
        self.distance_threshold = distance_threshold
        self.rng = np.random.default_rng()

    def __iter__(self):
        return iter(self.generation)

    def __getitem__(self, index):
        return self.generation[index]
    
    def get_next_generation():
        next_generation = Generation()
        species = self.speciation()
        number_of_offspring = GENERATION_SIZE
        population_average_adjusted_fitness = sum([calulate_total_adjusted_fitness(species[species_number]) for species_number in species]) / self.size
        
        number_of_offspring = GENERATION_SIZE
        for species_number in species:
            allowed_number_of_offspring = min(round((calulate_total_adjusted_fitness(species[species_number]) * len(species[species_number]) / population_average_adjusted_fitness)), number_of_offspring)
            number_of_offspring -= allowed_number_of_offspring

            for i in repeat(number_of_offspring):
                mating_pool = roulette_wheel_selection(species[species_number])


            


        
    def speciation(self):
        current_species_number = 0
        genomes = self.copy()
        species = {}
        while genomes:
            current_species_number += 1
            random_genome = choice(genomes, 1)[0]
            genomes.remove(random_genome)
            species[current_species_number] = [random_genome]
            
            for genome in genomes[:]:
                if self.get_distance_between_2_genomes(random_genome, genome) < self.distance_threshold:
                    species[current_species_number].append(genome)
                    genomes.remove(genome)
        return species



    def roulette_wheel_selection(self, genomes, mating_pool_size=2):
        mating_pool = []
        
        max_percent_genomes = sorted([genome for genome in genomes], key=fitness_function)[-int(self.size * PERCENTAGE_OF_GENOMES_ALLOWED_TO_REPRODUCE):]
        
        max_percent_genome_fitness_values = sorted([fitness_function(genome) for genome in genomes])[-int(self.size * PERCENTAGE_OF_GENOMES_ALLOWED_TO_REPRODUCE):]
        total_max_percent_species_fitness = sum(max_percent_genome_fitness_values)

        genome_selection_probability =[(genome_fitness_value / total_max_species_fitness) for genome_fitness_value in max_percent_genome_fitness_values]

        return self.rng.choice(max_percent_genomes, p=genome_selection_probability,size=mating_pool_size), total_species_fitness / len(chromosome_fitness_values)
        


    def crossover(self, parent1, parent2):
        fittest_parent = max(genome1, genome2, key=fitness_function)
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

        genome_1_maximum_innovation_id = max([connection_gene.innovation_id for connection_gene in genome1.connection_genes]), 
        genome_2_maximum_innovation_id = max([connection_gene.innovation_id for connection_gene in genome2.connection_genes])
        
        for connection_gene_1 in genome1.connection_genes:
            if connection_gene_1.innovation_id not in [connection_gene_2.innovation_id for connection_gene_2 in genome2.connection_genes]:
                genome_1_excess_and_disjoint_connection_genes.append(connection_gene_1)

        for connection_gene_2 in genome2.connection_genes:
            if connection_gene_2.innovation_id not in [connection_gene_1.innovation_id for connection_gene_1 in genome1.connection_genes]:
                genome_2_excess_and_disjoint_connection_genes.append(connection_gene_2)

        for connection_gene_1 in genome_1_excess_and_disjoint_connection_genes:
            if connection_gene_1.innovation_id > genome_2_maximum_innovation_id:
                excess_connection_genes.append(connection_gene_1)
        for connection_gene_2 in genome_2_excess_and_disjoint_connection_genes:
            if connection_gene_2.innovation_id > genome_1_maximum_innovation_id:
                excess_connection_genes.append(connection_gene_2)


    def get_number_of_excess_and_disjoint_connection_genes(self, genome1, genome2):
        #Will need to be able to get the exxcess and disjoint connections later
        number_of_excess_and_disjoint_connection_genes = 0
        for connection_gene_1 in genome1.connection_genes:
            if connection_gene_1.innovation_id not in [connection_gene_2.innovation_id for connection_gene_2 in genome2.connection_genes if connection_gene_2.enabled] and connection_gene_1.enabled:
                number_of_excess_and_disjoint_connection_genes += 1

        for connection_gene_2 in genome2.connection_genes:
            if connection_gene_2.innovation_id not in [connection_gene_1.innovation_id for connection_gene_1 in genome1.connection_genes if connection_gene_1.enabled] and connection_gene_2.enabled:
                number_of_excess_and_disjoint_connection_genes += 1

        return number_of_excess_and_disjoint_connection_genes

                                               
    def get_distance_between_2_genomes(self, genome1, genome2):
        #Could Normalise the Number of Excess and Disjoint Connections by N
        return self.get_number_of_excess_and_disjoint_genes(genome1, genome2) +  self.get_average_enabled_weight_difference(
            genome1, genome2)


def copy_genome(genome):
    copied_genome = Genome()
    copied_genome.node_genes = genome.node_genes.copy()
    copied_genome.connection_genes = genome.connection_genes.copy()
    return copied_genome

def get_weights_of_shared_connections(genome1, genome2):
    return [(connection_gene_1.weight, connection_gene_2.weight) for connection_gene_1 in genome1.connection_genes for connection_gene_2 in genome2.connection_genes if connection_gene_1.innovation_id == connection_gene_2.innovation_id]


def get_average_enabled_weight_difference(self, genome1, genome2):
        weights_of_shared_connections = get_weights_of_shared_connections()
        return sum(abs(weight_1 - weight_2) for weight_1, weight_2 in weights_of_shared_connections) / len(weights_of_shared_connections)

def calulate_total_adjusted_fitness(genomes):
    return sum([fitness_function(genome) / len(species) for genome in genomes])

def fitness_function():
    pass


