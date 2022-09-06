from functools import partial
from math import copysign

from calc import move_towards
from constants import TARGET_FPS, FPS

sign = partial(copysign, 1)


class IDLE:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        if self.entity.direction.x:
            return RUN(self.entity)

        if self.entity.events["up"] and self.entity.air_timer <= self.entity.JUMP_GRACE_TIME:
            return JUMP(self.entity)

        return self

    def process_x_movement(self, dt):
        return self

    def process_y_movement(self, dt):
        self.entity.velocity.y = calculate_y_velocity(self.entity)
        if self.entity.grounded:
            if self.entity.velocity.x == 0 and not self.entity.direction.x:
                return self
            else:
                return RUN(self.entity)
        else:
            return FALL(self.entity)


class RUN:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        if self.entity.events["up"] and self.entity.air_timer <= self.entity.JUMP_GRACE_TIME:
            return JUMP(self.entity)

        if self.entity.velocity.x == 0 and not self.entity.direction.x:
            return IDLE(self.entity)

        return self
        # TODO add dash

    def process_x_movement(self, dt):
        if self.entity.velocity.x == 0 and not self.entity.direction.x:
            return IDLE(self.entity)

        self.entity.velocity.x = calculate_x_velocity(self.entity)
        return self

    def process_y_movement(self, dt):
        self.entity.velocity.y = calculate_y_velocity(self.entity)
        if self.entity.grounded:
            if self.entity.velocity.x == 0 and not self.entity.direction.x:
                return IDLE(self.entity)
            else:
                return self
        else:
            return FALL(self.entity)


class DASH:
    def __init__(self, entity):
        self.entity = entity
        self.dash_timer = entity.DASH_TIME

    def input_handler(self):
        return self

    def process_x_movement(self, dt):
        self.dash_timer -= dt
        self.entity.velocity.x = calculate_x_velocity(self.entity)

    def process_y_move


class JUMP:
    def __init__(self, entity):
        self.entity = entity
        self.entity.y_heights = []

    def process_y_movement(self, dt):
        self.entity.velocity.y = self.entity.INIT_JUMP_VELOCITY
        self.entity.grounded = False
        self.entity.can_jump = False
        self.entity.air_timer += dt
        return FALL(self.entity)

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity)

        return self


class FALL:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        if self.entity.events["up"] and self.entity.air_timer <= self.entity.JUMP_GRACE_TIME and self.entity.can_jump:
            return JUMP(self.entity)

        return self

    def process_y_movement(self, dt):
        self.entity.velocity.y = calculate_y_velocity(self.entity)
        if self.entity.grounded:
            if self.entity.velocity.x == 0 and not self.entity.direction.x:
                return IDLE(self.entity)
            else:
                return RUN(self.entity)

        self.entity.air_timer += dt
        return self

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity)

        return self


def calculate_x_velocity(entity):
    mult = 1
    target_velocity = entity.MAX_RUN * entity.direction.x
    if abs(target_velocity) < 0.01:
        vel_power = entity.STOP_POWER
    elif abs(entity.velocity.x) > 0 and sign(target_velocity) != sign(entity.velocity.x):
        vel_power = entity.TURN_POWER
    else:
        vel_power = entity.ACCEL_POWER

    accel_rate = pow((entity.ACCEL_RUN / TARGET_FPS), vel_power)
    if entity.is_dashing:
        mult = entity.RUN_REDUCE
    return move_towards(entity.velocity.x, target_velocity, accel_rate * mult)


def calculate_y_velocity(entity):
    if entity.velocity.y < 0:
        mult = 1
    else:
        mult = 0.5
    return move_towards(entity.velocity.y, entity.MAXFALL, (entity.GRAVITY * mult) / FPS)
