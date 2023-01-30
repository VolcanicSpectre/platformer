from pathlib import Path
from pygame.mixer import Sound
import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sound_effects: dict[str, Sound] = {}
        self.bgm_volume: float = 1.0
        self.sfx_volume: float = 1.0
        self.current_bgm = None

    def load_sound(self, name: str, path: Path):
        """Loads a sound effect into the sound effects

        Args:
            name (str): The name of the sound effect which will be used as the key in the sound effects dictionary
            path (Path): The path to the sound effect
        """
        self.sound_effects[name] = Sound(path)

    def play_sound(self, name: str):
        """Plays the specified sound effect

        Args:
            name (str): The name of the sound effect to be played
        """
        sound = self.sound_effects.get(name)
        if sound:
            sound.set_volume(self.sfx_volume)
            sound.play()

    def set_bgm(self, file: Path):
        """Sets the backgroudn music

        Args:
            file (Path): The path to background music
        """
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(self.bgm_volume)
        pygame.mixer.music.play(-1)
        self.current_bgm = file

    def stop_bgm(self):
        """Stops the background music from playing"""
        pygame.mixer.music.stop()

    def set_bgm_volume(self, volume: float):
        """Sets the volume of the background music

        Args:
            volume (float): The new volume for the background music
        """
        self.bgm_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sfx_volume(self, volume: float):
        """Sets the volume for all sound effects

        Args:
            volume (float): The new volume for all sound effects
        """
        self.sfx_volume = volume
