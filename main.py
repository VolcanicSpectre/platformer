import cProfile
from platformer.platformer import Platformer
from platformer.config import PlatformerConfig


def main(profile: cProfile.Profile =None):
    platformer = Platformer(config)
    running = True
    while running:
        platformer.update()


if __name__ == "__main__":
    config = PlatformerConfig()
    if config.debug:
        with cProfile.Profile() as profile:
            main(profile)
    else: 
        main()
        