from os import path
from time import strftime

DEBUG = False
DEBUG_FILENAME = (strftime("%m-%d-%Y")) + "_RENDER_QUEUE_CAP_120.prof"
WIDTH, HEIGHT = 1920, 1080
DS_WIDTH, DS_HEIGHT = 576, 320
FPS = 120
TARGET_FPS = 120

# Map
CHUNK_SIZE = 4
TILE_SIZE = 16

# Directories
GAME_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(GAME_FOLDER, "assets")
MAP_FOLDER = path.join(ASSETS_FOLDER, "maps")
PLAYER_FOLDER = path.join(ASSETS_FOLDER, "player")

# Neural Network
z = 0.01

NUM_STACKED_FRAMES = 4
MEMORY_BUFFER_MAX_SIZE = 2000

INITIAL_GAMMA_VALUE = 0.6
INITIAL_EPSILION_VALUE = 0.1

KERNEL_SIZES = ((32, 8, 8), (64, 4, 4), (64, 3, 3))
STRIDES = (4, 2, 1)
DENSE_OUTPUT_SIZES = (512, 4)