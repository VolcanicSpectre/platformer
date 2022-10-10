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


INITIAL_SIZES = (720, 1, 4)
NUMBER_OF_GENERATIONS = 1
ALLOW_RECURRENT_CONNECTIONS = True

MUTATE_WEIGHTS_CHANCE = 0.8
PLUS_OR_MINUS_20_PERCENT_CHANCE = 0.9
COMPLETY_MUTATE_WEIGHT = 0.1
ENABLE_CONNECTION_CHANCE = 0.25