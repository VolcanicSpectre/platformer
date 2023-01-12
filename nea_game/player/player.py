from os.path import isdir
from os import listdir
from pathlib import Path
from pygame.image import load
from pygame import Surface
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

    def __init__(self, player_folder: Path):
        self.idle_state = PlayerIdleState(self, "idle")
        self.run_state = PlayerRunState(self, "run")
        self.jump_state = PlayerJumpState(self, "jump")

        frames = {}

        for folder in listdir(player_folder):
            if isdir((player_folder / folder)):
                print(folder)
                frames[folder] = [
                    load(player_folder / (f"{folder}/{image_name}"))
                    for image_name in listdir(player_folder / folder)
                ]

        self.renderer = AnimatedRenderer(frames)
        # self.input = Input(PlayerActionSpace)
        self.rb = RigidBody2D(5, 3)

        self.x_run_speed = 5
        self.acceleration_rate = 2
        self.deceleration_rate = 5
        self.velocity_power = 0.6

        self.friction = 2

    def start(self):
        """Creates the PlayerPlayerState machine for the player"""
        self.state_machine = StateMachine(self.idle_state)

    def update(self, dt: float):
        pass
        # x_velocity_component = near_zero(self.rb.velocity.x)
        # y_velocity_component = near_zero(self.rb.velocity.y)
        # self.rb.velocity = Vector2D(x_velocity_component, y_velocity_component)

        # self.state_machine.get_current_state().update(dt)
