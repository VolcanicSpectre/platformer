from os import system
from nea_game.config import NeaGameConfig

if __name__ == "__main__":
    config = NeaGameConfig()
    if config.debug:
        system(f"python app.py --fname {config.debug_file}")
    else:
        system("python app.py")
        