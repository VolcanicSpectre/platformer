from os import path
from platformer.config import PlatformerConfig
from platformer.gui.root import Root
from platformer.menu.main_menu import MainMenu


class Platformer(Root):
    def __init__(self, config: PlatformerConfig):
        self.config = config
        super().__init__(self.config.resoloution, self.config.internal_resoloution)
        self.windows[MainMenu] = MainMenu(
            self.screen,
            self.display_surface,
            path.join(config.directories["background"]),
        )

        self.show_window(MainMenu)
