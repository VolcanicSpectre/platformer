from os import path
from time import strftime

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
WORLDS_FOLDER = path.join(ASSETS_FOLDER, "worlds")
PLAYER_FOLDER = path.join(ASSETS_FOLDER, "player")
