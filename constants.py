from os import path
from time import strftime

DEBUG = False
DEBUG_FILENAME = (strftime("%m-%d-%Y")) + "_FRAMERATE_INDEPENDENCE.prof"
WIDTH, HEIGHT = 1920, 1080
DS_WIDTH, DS_HEIGHT = 576, 320
FPS = 120
TARGET_FPS = 120
CHUNK_SIZE = 4
TILE_SIZE = 16
GAME_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(GAME_FOLDER, "assets")
MAP_FOLDER = path.join(ASSETS_FOLDER, "maps")
PLAYER_FOLDER = path.join(ASSETS_FOLDER, "player")
