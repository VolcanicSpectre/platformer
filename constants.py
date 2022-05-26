from os import path
DEBUG = True
WIDTH, HEIGHT = 1152, 640
DS_WIDTH , DS_HEIGHT = 576, 320
FPS = 1000
CHUNK_SIZE = 4
GAME_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(GAME_FOLDER, "assets")
MAP_FOLDER = path.join(ASSETS_FOLDER, "maps")
PLAYER_FOLDER = path.join(ASSETS_FOLDER, "player")