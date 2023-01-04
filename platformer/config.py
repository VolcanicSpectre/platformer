"""Provides an interface for storing and loading game wide values"""
from json import load
from pathlib import Path
from time import strftime


class PlatformerConfig:
    """Handles loading of the settings.json file"""

    debug: bool
    debug_file: str

    directories: dict[str, Path]

    resoloution: tuple[int, int]
    internal_resoloution: tuple[int, int]

    fps: int
    internal_fps: int

    chunk_size: int

    def __init__(self):
        # Debug
        self.debug = False
        debug_filename = ""
        self.debug_file = (strftime("%m-%d-%Y")) + debug_filename

        # Directories
        platformer_folder = Path(__file__).absolute().parent
        game_folder = platformer_folder.parent
        assets_folder = game_folder / "assets"
        background_folder = assets_folder / "background"
        player_folder = assets_folder / "player"
        worlds_folder = assets_folder / "worlds"

        self.directories = {
            "game": game_folder,
            "assets": assets_folder,
            "background": background_folder,
            "player": player_folder,
            "worlds": worlds_folder,
            "platformer": platformer_folder,
        }

        # Display
        width = self.get_int_setting("x_resolution")
        height = self.get_int_setting("y_resolution")
        self.resoloution = (width, height)

        ds_width = 384
        ds_height = 216
        self.internal_resoloution = (ds_width, ds_height)

        self.fps = self.get_int_setting("fps")
        self.internal_fps = 60

        # World
        self.chunk_size = 4

    def get_int_setting(self, setting: str) -> int:
        """_summary_

        Args:
            setting (str): the identifier of the setting in [settings.json]

        Raises:
            ValueError: If the value of the specified setting is not of type [int]

        Returns:
            int: The value of the specified setting
        """
        with (self.directories["platformer"] / "settings.json").open(
            mode="r"
        ) as settings_json:
            settings = load(settings_json)
            if isinstance(settings[setting], int):
                return settings[setting]

            raise ValueError

    def get_float_setting(self, setting: str) -> float:
        """_summary_

        Args:
            setting (str): the identifier of the setting in [settings.json]

        Raises:
            ValueError: If the value of the specified setting is not of type [float]  or [int]

        Returns:
            float: The value of the specified setting
        """
        with (self.directories["platformer"] / "settings.json").open(
            mode="r"
        ) as settings_json:
            settings = load(settings_json)
            if isinstance(settings[setting], (float, int)):
                return settings[setting]

            raise ValueError