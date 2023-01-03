import cProfile
from platformer.menu.platformer import Platformer
from platformer.config import PlatformerConfig


def main(pr=None):
    platformer = Platformer(config)
    running = True
    while running:
        platformer.update()


if __name__ == "__main__":
    config = PlatformerConfig()
    if config.debug:
        with cProfile.Profile() as pr:
            main(pr)
    else:
        main()