import cProfile
from nea_game.nea_game import NeaGame
from nea_game.config import NeaGameConfig
from nea_game.ldtk_world_loader.tileset import Tileset
from json import load


def main(profile: cProfile.Profile = None):
    nea_game = NeaGame(config)
    running = True
    while running:
        nea_game.update()


if __name__ == "__main__":
    config = NeaGameConfig()
    with (config.directories["worlds"] / "1.json").open() as j:
        data = load(j)

    t = Tileset(data["defs"]["tilesets"][0], config.directories["worlds"])
    if config.debug:
        with cProfile.Profile() as profile:
            main(profile)
    else:
        main()
