from numpy.random import default_rng
from functools import lru_cache
from pickle import dump, load
from constants import *
from connection_types import ConnectionTypes
from node_types import NodeTypes
import json
from collections import defaultdict, OrderedDict
#import pygame
import sys

sys.setrecursionlimit(9999999)

# class Generation:
#     def __init__(self, number, distance_threshold):
#         self.connections = {}
#         self.current_innovation = 0
#         self.rng = default_rng()

class Genome:
    def __init__(self, generation, blank_initialise=True): 
        self.rng = default_rng()
        self.generation = generation
        self.fitness = 0
        self.node_genes = []
        self.connection_genes = []
        self.outputs = []
        if not blank_initialise:
            self.initilaise()
    
    def __lt__(self, other):
        return self.fitness < other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness
    
    def initilaise(self):
        valid_genome = False 
        while not valid_genome:
            
            temp_connections_dict = self.generation.connections.copy()
            
            self.node_genes = [NodeGene(i, 0, NodeTypes.INPUT) for i in range(INITIAL_SIZES[0])]
            node_gene_counter = len(self.node_genes)
            
            self.node_genes += [NodeGene(i + node_gene_counter, 1, NodeTypes.HIDDEN) for i in range(INITIAL_SIZES[1])]
            node_gene_counter = len(self.node_genes)
            
            self.node_genes += [NodeGene(i + node_gene_counter, 2,  NodeTypes.OUTPUT) for i in range(INITIAL_SIZES[2])]
            for input_node in [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.INPUT]:
                for hidden_node in [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.HIDDEN]:
                    if self.rng.uniform(size=1) < PERCENTAGE_OF_INITIAL_CONNECTIONS:
                        try:
                            innovation_id = self.generation.connections[(input_node.id, hidden_node.id)]
                        except KeyError:
                            innovation_id = self.generation.current_innovation
                            self.generation.connections[(input_node.id, hidden_node.id)] = innovation_id
                            self.generation.current_innovation += 1
                    
                        self.connection_genes.append(ConnectionGene(innovation_id, input_node.id, hidden_node.id, self.rng.uniform(low=-20, high=20, size=1)[0]))
            
            for hidden_node in [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.HIDDEN]:
                for output_node in [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.OUTPUT]:
                    if self.rng.uniform(size=1) < PERCENTAGE_OF_INITIAL_CONNECTIONS:
                        try:
                            innovation_id = self.generation.connections[(hidden_node.id, output_node.id)]
                        except KeyError:
                            innovation_id = self.generation.current_innovation
                            self.generation.connections[(hidden_node.id, output_node.id)] = innovation_id 
                            self.generation.current_innovation += 1
                            
                        self.connection_genes.append(ConnectionGene(innovation_id, hidden_node.id, output_node.id, 5))
    
            try:
                self.set_node_layers()
            except ValueError: # There is no valid path to the input layer
                self.generation.connections = temp_connections_dict

                self.node_genes = []
                self.connection_genes = []
                self.outputs = []
            else:
                valid_genome = True
 
    def feed_forward(self, inputs):
        self.outputs = []
        self.set_node_layers()        
        
        node_genes_by_layer = defaultdict(list)
        for node_gene in self.node_genes:
            node_genes_by_layer[node_gene.layer].append(node_gene)
        
        node_genes_by_layer = dict(sorted(node_genes_by_layer.items()))
        output_layer = max(node_genes_by_layer)

        for input_node, input_value in zip(node_genes_by_layer[0], inputs):
            input_node.input_value = 0
            input_node.input_value = input_value
            
            for connection_gene_terminating_at_node in [connection_gene for connection_gene in self.connection_genes if connection_gene.output_node_id == input_node.id]:
                input_node.input_value += self.node_genes[connection_gene_terminating_at_node.input_node_id].output_value * connection_gene_terminating_at_node.weight    
            
            input_node.output_value = input_node.input_value
        

        del(node_genes_by_layer[0])
        
        for layer in node_genes_by_layer.values():
            for node_gene in layer:
                node_gene.input_value = 0
                for connection_gene_terminating_at_node in [connection_gene for connection_gene in self.connection_genes if connection_gene.output_node_id == node_gene.id]:
                    node_gene.input_value += self.node_genes[connection_gene_terminating_at_node.input_node_id].output_value * connection_gene_terminating_at_node.weight
                
                node_gene.output_value = node_gene.activation_function(node_gene.input_value)

        #temp_var = [node_gene.output_value for node_gene in node_genes_by_layer[output_layer]]
        for node_gene in node_genes_by_layer[output_layer]:
            self.list_of_outputs.append(node_gene.output_value)
    
    def mutate(self):
        self.set_node_layers()
        seed = self.rng.uniform(size=1)
        if seed < ADD_NODE_CHANCE:
            self.mutate_add_node()
        elif seed < ADD_CONNECTION_CHANCE:
            self.mutate_add_connection()
        elif seed < MUTATE_WEIGHTS_CHANCE:
            self.mutate_weights()

    def mutate_weights(self):
        for connection_gene in self.connection_genes:
            seed = self.rng.uniform(size=1)
            if seed < COMPLETELY_MUTATE_WEIGHT_CHANCE:
                connection_gene.weight +=self.rng.uniform(-MUTATION_POWER, MUTATION_POWER, 1)[0]
            else:
                connection_gene.weight = self.rng.uniform(-20, 20, 1)[0]

    def mutate_add_connection(self):
        connection_found = False
        for i in range(20):
            if connection_found:
                break
            node_gene_1, node_gene_2 = [self.rng.choice(self.node_genes, 1)[0] for i in range(2)]
            connection_type = self.valid_node_pair(node_gene_1, node_gene_2)

            if connection_type:
                connection_found = True
                if connection_type == ConnectionTypes.CONNECTION_EXISTS:
                    connection = [connection_gene for connection_gene in self.connection_genes if (
                            connection_gene.input_node_id == node_gene_1.id and connection_gene.output_node_id == node_gene_2.id)][0]
                    
                    if not connection.enabled:
                        if self.rng.uniform(size=1) < ENABLE_CONNECTION_CHANCE:
                            connection.enabled = True
                else:
                    try:
                        innovation_id = self.generation.connections[(node_gene_1.id, node_gene_2.id)]
                    except KeyError:
                        innovation_id = self.generation.current_innovation
                        self.generation.current_innovation += 1
                    
                    if self.rng.uniform(size=1) < RECURRENT_CONNECTION_CHANCE:
                        recurrent = True
                        if connection_type != ConnectionTypes.RECURRENT:
                            node_gene_1, node_gene_2 = node_gene_2, node_gene_1
                    else:
                        recurrent = False
                        if connection_type == ConnectionTypes.RECURRENT:
                            node_gene_1, node_gene_2 = node_gene_2, node_gene_1
                    
                    
                    
                    self.connection_genes.append(ConnectionGene(innovation_id, node_gene_1.id, node_gene_2.id, self.rng.uniform(low=-20, high=20, size=1)[0], recurrent=connection_type == recurrent))

    def valid_node_pair(self, node_gene_1, node_gene_2):
        if [connection_gene for connection_gene in self.connection_genes if
            (connection_gene.input_node_id == node_gene_1.id and connection_gene.output_node_id == node_gene_2.id)]:
            return ConnectionTypes.CONNECTION_EXISTS
        if node_gene_1.id == node_gene_2.id:
            return False
        if node_gene_1.layer == node_gene_2.layer:
            return False
        if node_gene_1.layer > node_gene_2.layer:
            if ALLOW_RECURRENT_CONNECTIONS:
                return ConnectionTypes.RECURRENT
            else:
                return False

        return ConnectionTypes.VALID_FORWARD_CONNECTION

    def mutate_add_node(self):
        connection_for_new_node = self.rng.choice([connection_gene for connection_gene in self.connection_genes if not connection_gene.recurrent])
        connection_for_new_node.enabled = False
        new_node_gene = NodeGene(len(self.node_genes))
        

        try:
            innovation_id = self.generation.connections[(connection_for_new_node.input_node_id, new_node_gene.id)]
        except KeyError:
            innovation_id = self.generation.current_innovation
            self.generation.current_innovation += 1
        
        new_connection_gene_1 = ConnectionGene(innovation_id, connection_for_new_node.input_node_id, new_node_gene.id, self.rng.uniform(low=-20, high=20, size=1)[0])
        

        try:
            innovation_id = self.generation.connections[(new_node_gene.id, connection_for_new_node.output_node_id)]
        except KeyError:
            innovation_id = self.generation.current_innovation
            self.generation.current_innovation += 1

        new_connection_gene_2 = ConnectionGene(innovation_id, new_node_gene.id, connection_for_new_node.output_node_id, self.rng.uniform(low=-20, high=20, size=1)[0])
        
        self.connection_genes.append(new_connection_gene_1)
        self.connection_genes.append(new_connection_gene_2)
        self.node_genes.append(new_node_gene)

    def set_node_layers(self):
        max_layer = -1
        for node_gene in [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.HIDDEN]:
            node_gene.layer = self.get_longest_path_to_input_layer(node_gene)
            if node_gene.layer > max_layer:
                max_layer = node_gene.layer

        for output_node_gene in [node_gene for node_gene in self.node_genes if node_gene.type_ == NodeTypes.OUTPUT]:
            output_node_gene.layer = max_layer + 1

    def get_longest_path_to_input_layer(self, node_gene):
        path_lengths = []
        
        for connection_termianting_at_node in [connection_gene for connection_gene in self.connection_genes if (not connection_gene.recurrent) and connection_gene.output_node_id == node_gene.id]:
            if self.node_genes[connection_termianting_at_node.input_node_id].type_ == NodeTypes.INPUT:
                path_lengths.append(1)
            else:
                path_lengths.append(
                    1 + self.get_longest_path_to_input_layer(
                        self.node_genes[connection_termianting_at_node.input_node_id]))

        return max(path_lengths)

    def draw(self, screen):
        self.set_node_layers()
        columns = max([node_gene.layer for node_gene in self.node_genes])
        rows = defaultdict(list)
        for node_gene in self.node_genes:
            rows[node_gene.layer].append(node_gene)
        rows = dict(sorted(rows.items()))

        column_width = 1920 // (columns + 1)
        row_heights_dict = {layer_number: (1080//nodes_in_layer) for layer_number, nodes_in_layer in zip(rows.keys(), [len(node_genes) for node_genes in rows.values()])}
        column_pixels = list(range(0, 1921, column_width))
        row_pixels = {layer_number:list(range(0, 1081, row_height)) for layer_number, row_height in zip(row_heights_dict.keys(), row_heights_dict.values())}
        
        nodes_to_draw = {}
        for layer_number, column_pixel in zip(rows, column_pixels):
            for node, row_pixel in zip(rows[layer_number], row_pixels[layer_number]):
                if node.type_ == NodeTypes.INPUT:
                    colour = (0, 255, 0)
                elif node.type_ == NodeTypes.HIDDEN:
                    colour = (0, 0, 255)
                elif node.type_ == NodeTypes.OUTPUT:
                    colour = (255, 0, 0)

                box_rect = pygame.Rect(column_pixel, row_pixel, column_width, row_heights_dict[layer_number])
                radius = min(box_rect.width, box_rect.height) // 4  
                nodes_to_draw[node.id] = (colour, box_rect.center, radius)

        for node_id, params in zip(nodes_to_draw.keys(), nodes_to_draw.values()):
            colour, center, radius = params
            pygame.draw.circle(screen, colour, center, radius)
            for connection_gene in [connection_gene for connection_gene in self.connection_genes if node_id == connection_gene.input_node_id]:
                if connection_gene.enabled:
                    for node_id_2 in nodes_to_draw:
                        if node_id_2 == connection_gene.output_node_id:
                            if connection_gene.recurrent:
                                colour = (173, 216, 230)
                            else:
                                colour = (20, 200 ,50)
                            target_center = nodes_to_draw[node_id_2][1]
            
                    pygame.draw.line(screen, colour, center, target_center, 2)


    def save_genome(self):
        with open(f"{self.generation.generation_number}_{self.generation.generation.index(self)}.pickle", "wb") as f:
            dump(self, f)








class NodeGene:
    def __init__(self, id, layer=0, type_=NodeTypes.HIDDEN, activation_function=sigmoid):
        self.id = id
        self.layer = layer
        self.type_ = type_
        self.input_value = 0
        self.output_value = 0
        self.activation_function = activation_function


class ConnectionGene:
    def __init__(self, innovation_id, input_node_id, output_node_id, weight, enabled=True, recurrent=False):
        self.innovation_id = innovation_id
        self.input_node_id = input_node_id
        self.output_node_id = output_node_id
        self.weight = weight
        self.enabled = enabled
        self.recurrent = recurrent

    def __str__(self):
        print(f"({self.input_node_id} -> {self.output_node_id}) : {self.weight}")



def load_genome(file_path):
    with open(file_path, "rb") as f:
        return load(f)

if __name__ == '__main__':
    width, height = 1920, 1080

    screen = pygame.display.set_mode((width, height))
    gen = Generation(0, 4)
    test_genome = Genome(gen, blank_initialise=False)
    running = True
    while running:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    test_genome.mutate_add_node()
                elif event.key == pygame.K_o:
                    test_genome.mutate_add_connection()
        test_genome.set_node_layers()
        test_genome.draw(screen)
        pygame.display.update()
    
