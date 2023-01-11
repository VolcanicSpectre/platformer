"""Provides an interface for storing and loading game wide values"""
from json import load
from pathlib import Path
from time import strftime


class NeaGameConfig:
    """Handles loading of the config.json file"""

    debug: bool
    debug_file: str

    directories: dict[str, Path]

    resoloution: tuple[int, int]
    internal_resoloution: tuple[int, int]

    fps: int
    internal_fps: int

    chunk_size: int

    key_bindings: list[int]

    unlocked_levels: list[bool]

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
        buttons_folder = assets_folder / "buttons"
        player_folder = assets_folder / "player"
        worlds_folder = assets_folder / "worlds"

        self.directories = {
            "game": game_folder,
            "assets": assets_folder,
            "background": background_folder,
            "buttons": buttons_folder,
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

        self.key_bindings = self.get_integer_list_setting("key_bindings")

        self.unlocked_levels = self.get_bool_list_setting("unlocked_levels")

    def get_int_setting(self, setting: str) -> int:
        """_summary_

        Args:
            setting (str): the identifier of the setting in [config.json]

        Raises:
            ValueError: If the value of the specified setting is not of type [int]

        Returns:
            int: The value of the specified setting
        """
        with (self.directories["platformer"] / "config.json").open(
            mode="r"
        ) as settings_json:
            settings = load(settings_json)
            if isinstance(settings[setting], int):
                return settings[setting]

            raise ValueError

    def get_float_setting(self, setting: str) -> float:
        """_summary_

        Args:
            setting (str): the identifier of the setting in [config.json]

        Raises:
            ValueError: If the value of the specified setting is not of type [float]  or [int]

        Returns:
            list[int]: The value of the specified setting
        """
        with (self.directories["platformer"] / "config.json").open(
            mode="r"
        ) as settings_json:
            settings = load(settings_json)
            if isinstance(settings[setting], (float, int)):
                return settings[setting]

            raise ValueError

    def get_integer_list_setting(self, setting: str) -> list[int]:
        """Gets the relevant setting from config.json that is a list of integers

        Args:
            setting (str): the identifier of the setting in [config.json]

        Raises:
            ValueError: If the value of the specified setting is not of type [float] or [int]

        Returns:
            list[int]: The value of the specified setting
        """
        with (self.directories["platformer"] / "config.json").open(
            mode="r"
        ) as settings_json:
            settings = load(settings_json)
            if all(isinstance(element, int) for element in settings[setting]):
                return settings[setting]

            raise ValueError

    def get_bool_list_setting(self, setting: str) -> list[bool]:
        """Gets the relevant setting from config.json that is a list of bools

        Args:
            setting (str): the identifier of the setting in [config.json]

        Raises:
            ValueError: If the value of the specified setting is not of type [bool]

        Returns:
            list[bool]: The value of the specified setting
        """
        with (self.directories["platformer"] / "config.json").open(
            mode="r"
        ) as settings_json:
            settings = load(settings_json)
            if all(isinstance(element, bool) for element in settings[setting]):
                return settings[setting]

            raise ValueError

    def reload(self):
        """Reloads the settings from config.json"""
        width = self.get_int_setting("x_resolution")
        height = self.get_int_setting("y_resolution")
        self.resoloution = (width, height)

        self.fps = self.get_int_setting("fps")

        self.key_bindings = self.get_integer_list_setting("key_bindings")
