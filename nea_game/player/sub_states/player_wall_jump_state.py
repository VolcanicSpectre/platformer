from nea_game.calc.vector2d import Vector2D
from nea_game.components.rigidbody2d import ForceMode
from nea_game.player.super_states.player_ability_state import PlayerAbilityState


class PlayerWallJumpState(PlayerAbilityState):
    def enter(self):
        super().enter()
 