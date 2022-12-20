"""Provides an interface for storing and loading game wide values"""
from json import load
from os import path
from time import strftime


class PlatformerConfig:
    """Handles loading of the settings.json file"""

    def __init__(self):
        # Debug
        self.__debug = False
        debug_filename = ""
        self.__debug_file = (strftime("%m-%d-%Y")) + debug_filename

        # Directories
        game_folder = path.dirname(__file__)
        assets_folder = path.join(game_folder, "assets")
        player_folder = path.join(assets_folder, "player")
        worlds_folder = path.join(assets_folder, "worlds")
        self.__directories = {
            "game": game_folder,
            "assets": "assets_folder",
            "player": player_folder,
            "worlds": worlds_folder,
        }

        # Display
        width = self.get_int_setting("x_resolution")
        height = self.get_int_setting("y_resolution")
        self.__resoloution = (width, height)

        ds_width = 576
        ds_height = 320
        self.__internal_resoloution = (ds_width, ds_height)

        self.__fps = self.get_int_setting("fps")
        self.__internal_fps = 60

        # World
        self.__chunk_size = 4

    @property
    def debug(self) -> bool:
        """A getter for debug

        Returns:
            bool: The value of debug
        """
        return self.__debug

    @property
    def debug_file(self) -> str:
        """A getter for debug_file

        Returns:
            str: The value of debug_file
        """
        return self.__debug_file

    @property
    def directories(self) -> dict[str, str]:
        """A getter for directories

        Returns:
            dict[str: str]: The value of directories
        """
        return self.__directories

    @property
    def resoloution(self) -> tuple[int, int]:
        """A getter for resoloution

        Returns:
            tuple[int, int]: The value of resoloution
        """
        return self.__resoloution

    @property
    def internal_resoloution(self) -> tuple[int, int]:
        """A getter for internal_resoloution

        Returns:
            tuple[int, int]: The value of resoloution
        """
        return self.__internal_resoloution

    @property
    def fps(self) -> int:
        """A getter for fps

        Returns:
            int: The value of fps
        """
        return self.__fps

    @property
    def internal_fps(self) -> int:
        """A getter for internal_fps

        Returns:
            int: The value of internal_fps
        """
        return self.__internal_fps

    @property
    def chunk_size(self) -> int:
        """A getter for chunk_size

        Returns:
            int: The value of chunk_size
        """
        return self.__chunk_size

    def get_int_setting(self, setting: str) -> int:
        """_summary_

        Args:
            setting (str): the identifier of the setting in [settings.json]

        Raises:
            ValueError: If the value of the specified setting is not of type [int]

        Returns:
            int: The value of the specified setting
        """
        with open(
            path.join(self.__directories["game"], "settings.json"), encoding="utf-8"
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
        with open(
            path.join(self.__directories["game"], "settings.json"), encoding="utf-8"
        ) as settings_json:
            settings = load(settings_json)
            if isinstance(settings[setting], (float, int)):
                return settings[setting]

            raise ValueError
