from os.path import isdir
from os import listdir
from pathlib import Path
from pygame.image import load
from pygame import Rect, Surface
from nea_game.calc.near_zero import near_zero
from nea_game.calc.vector2d import Vector2D
from nea_game.components.input import Input
from nea_game.components.renderer import AnimatedRenderer
from nea_game.components.rigidbody2d import RigidBody2D
from nea_game.entity.base_entity import BaseEntity
from nea_game.player.sub_states.player_idle_state import PlayerIdleState
from nea_game.player.sub_states.player_run_state import PlayerRunState
from nea_game.player.sub_states.player_jump_state import PlayerJumpState
from nea_game.player.player_action_space import PlayerActionSpace
from nea_game.states.player_state_machine import StateMachine


class Player(BaseEntity):
    frames: dict[str, list[Surface]]

    def __init__(self, player_folder: Path, action_bindings: list[int], x: int, y: int):
        """Defines player movement constants and starts the player in the idle state

        Args:
            player_folder (Path): The path to the player folder
            action_bindings (list[int]): The list of the key bindings for the player actions
            x (int): The x position of the player
            y (int): The y position of the player
        """
        super().__init__(x, y)

        self.idle_state = PlayerIdleState(self, "idle")
        self.run_state = PlayerRunState(self, "run")
        self.jump_state = PlayerJumpState(self, "jump")

        frames = {}

        for folder in listdir(player_folder):
            if isdir((player_folder / folder)):
                frames[folder] = [
                    load(player_folder / (f"{folder}/{image_name}"))
                    for image_name in listdir(player_folder / folder)
                ]

        self.renderer = AnimatedRenderer(frames)
        self.input = Input(PlayerActionSpace, action_bindings)
        self.rb = RigidBody2D(2, 3)
        self.state_machine = StateMachine(self.idle_state)

        self.rect = Rect((self.x, self.y), self.renderer.frames["idle"][0].get_size())

        self.x_run_speed = 3000
        self.acceleration_rate = 2
        self.deceleration_rate = 5
        self.velocity_power = 0.6

        self.friction = 2

    def input_handler(self):
        self.state_machine.current_state.input_handler()

    def update(self, dt: float):
        self.state_machine.current_state.update(dt)
        self.x += self.rb.velocity.x
        self.y += self.rb.velocity.y

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
