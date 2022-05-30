from enum import Enum
from math import copysign
from functools import partial

sign = partial(copysign, 1)


class States(Enum):
    NULL = 0
    IDLE = 1
    RUN = 2
    DASH = 3
    JUMP = 4
    FALL = 5


class State:
    def __init__(self, entity): self.entity = entity

    def handle_inputs(self, keys): return States.NULL

    def process_x_movement(self, dt): return States.NULL

    def process_y_movement(self, dt): return States.NULL


class IdleState(State):
    def handle_inputs(self):
        if self.entity.direction:
            return States.RUN
        if self.entity.events["up"]:
            return States.JUMP

        return States.NULL

    def process_y_movement(self, dt):
        self.entity.velocity.y += self.entity.FINAL_GRAVITY * dt
        if not self.entity.grounded:
            return States.FALL

        return States.NULL


class RunState(State):
    def handle_inputs(self):
        if self.entity.events["up"]:
            return States.JUMP
        return States.NULL
        # TODO add dash

    def process_x_movement(self, dt):

        if not self.entity.direction:
            return States.IDLE

        self.entity.velocity.x = calculate_x_velocity(self.entity, dt)

        return States.NULL

    def process_y_movement(self, dt):
        self.entity.velocity.y += self.entity.FINAL_GRAVITY * dt
        if not self.entity.grounded:
            return States.FALL

        return States.NULL


class DashState(RunState):
    DASHTIME = 0.4

    def __iter__(self):
        yield DashState.DASHTIME


class JumpState(State):
    def proceess_y_movement(self, dt):
        self.entity.velocity.y += self.entity.INIT_GRAVITY * dt

        if self.entity.grounded:
            if self.entity.direction:
                return States.RUN
            else:
                return States.IDLE

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity, dt)

        return States.NULL


class FallState(State):
    def proceess_y_movement(self, dt):
        self.entity.velocity.y += self.entity.FINAL_GRAVITY * dt

        if self.entity.grounded:
            if self.entity.direction:
                return States.RUN
            else:
                return States.IDLE

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity, dt)

        return States.NULL


def calculate_x_velocity(entity, dt):
    direction = entity.direction()
    u = entity.velocity.x
    target_speed = entity.MAXRUN * direction

    if abs(target_speed) > 0.01:
        a = entity.ACCELRUN
        if not entity.grounded:
            a *= 0.01
    else:
        a = entity.DECELRUN
        if not entity.grounded:
            a *= 0.6

    if (u > target_speed and target_speed > 0.01) or (u < target_speed and target_speed < -0.01):
        a = 0

    if abs(target_speed) < 0.01:
        vel_power = entity.STOPPOWER
    elif abs(u) > 0 and sign(target_speed) != sign(u):
        vel_power = entity.TURNPOWER
    else:
        vel_power = entity.ACCELPOWER

    v = (a*dt) ** vel_power

    if direction > 0:
        return min(u + v, target_speed)
    if direction < 0:
        return max(u + v*entity.x_move_input, target_speed)
    else:
        if sign(u) == -1:
            return min(u - (v*-1), target_speed*entity.dir)
        else:
            return max(u - v, target_speed*direction)
