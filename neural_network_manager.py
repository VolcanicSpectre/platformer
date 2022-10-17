from numpy.random import default_rng
from itertools import repeat
from constants import *
from genome import Genome


class Generation:
    """Pending Documentation"""

    def __init__(self, size):
        self.size = size
        self.generation = [Genome(INITIAL_SIZES) for i in repeat(self.size)]
        self.connections = {}
        self.current_innovation = 0
        self.distance_threshold = 4
        self.desired_number_of_species = 5
        self.rng = np.random.default_rng()

    def __iter__(self):
        return iter(self.generation)

    def __getitem__(self, index):
        return self.generation[index]
    
    def get_next_generation():
        species = self.speciation()
        for species_number in species:
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
        chromosome_fitness_values = [fitness_function(genome) for genome in genomes]
        total_population_fitness = sum(chromosome_fitness_values)

        chromosome_selection_probability =[(chromosome_fitness_value / total_population_fitness) for chromosome_fitness_value in chromosome_fitness_values]

        return self.rng.choice(genomes, p=chromosome_selection_probability,size=mating_pool_size)



        






    def reproduction(self, mating_pool):
        pass

    def crossover(self, parent1, parent2):
        pass


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

    def get_average_enabled_weight_difference(self, genome1, genome2):
        innovation_ids_of_shared_connections = [connection_gene_1.innovation_id for connection_gene_1 in
                                                genome1.connection_genes for connection_gene_2 in
                                                genome2.connection_genes if
                                                connection_gene_1.innovation_id == connection_gene_2.innovation_id]

    def get_distance_between_2_genomes(self, genome1, genome2):
        #Could Normalise the Number of Excess and Disjoint Connections by N
        return self.get_number_of_excess_and_disjoint_genes(genome1, genome2) +  self.get_average_enabled_weight_difference(
            genome1, genome2)


def fitness_function():
    pass


