from nea_game.nea_game import NeaGame
from nea_game.config import NeaGameConfig


def app():
    nea_game = NeaGame(config)

    running = True
    while running:
        nea_game.update()


if __name__ == "__main__":
    config = NeaGameConfig()
    app()
