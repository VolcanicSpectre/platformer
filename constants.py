from os import path
from time import strftime
from calc import relu, sigmoid, tanh

DEBUG = False
DEBUG_FILENAME = (strftime("%m-%d-%Y")) + "_RENDER_QUEUE_CAP_120.prof"
WIDTH, HEIGHT = 1920, 1080
DS_WIDTH, DS_HEIGHT = 576, 320
FPS = 120

# Map
TARGET_FPS = 120
CHUNK_SIZE = 4
TILE_SIZE = 16

# Directories
GAME_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(GAME_FOLDER, "assets")
MAP_FOLDER = path.join(ASSETS_FOLDER, "maps")
PLAYER_FOLDER = path.join(ASSETS_FOLDER, "player")

# Neural Network
ACTIVATION_FUNCTIONS = [relu, sigmoid, tanh]
CONNECTION_DTYPE = [("in", "u4"), ("out", "u4"), ("weight", "f8"), ("enabled", "?"), ("innovation", "u4")]
NEURON_DTYPE = [("id", "u4"), ("node_type", "u4"), ("node_layer", "u4"), ("sum_inp")]

INITIAL_SIZES = (720, 1, 4)
NUMBER_OF_GENERATIONS = 1

COMPLETY_MUTATE_WEIGHT = 0.1
VARIANCE_FOR_WEIGHT_MUTATION_MULTIPLIER = 0.1
