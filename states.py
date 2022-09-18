from functools import partial
from math import copysign
from pygame.math import Vector2

from calc import move_towards
from constants import TARGET_FPS, FPS

sign = partial(copysign, 1)


class IDLE:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        if self.entity.direction.x:
            return RUN(self.entity)

        if self.entity.events["dash"] and self.entity.can_dash and self.entity.direction != Vector2(0, 0):
            return DASH(self.entity, self.entity.direction)
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
        if self.entity.events["dash"] and self.entity.can_dash and self.entity.direction != Vector2(0, 0):
            return DASH(self.entity, self.entity.direction)

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
    def __init__(self, entity, dash_direction):
        self.entity = entity
        self.entity.can_dash = False
        self.entity.is_dashing = True
        self.dash_direction = dash_direction
        self.dash_timer = 0

    def input_handler(self):
        return self

    def process_x_movement(self, dt):
        self.dash_timer += dt
        if self.dash_timer > self.entity.DASH_DURATION:
            self.entity.is_dashing = False
            return FALL(self.entity)

        if self.dash_timer > self.entity.MIN_DASH_DURATION:
            self.entity.velocity.x = calculate_x_velocity(self.entity)
        else:
            self.entity.velocity.x = move_towards(self.entity.MAX_RUN * self.dash_direction.x,
                                                  pow(abs(self.entity.velocity.x),
                                                      self.entity.DASH_POWER) * self.dash_direction.x,
                                                  self.entity.DASH_ACCEL / TARGET_FPS)

    def process_y_movement(self, dt):
        if self.dash_timer > self.entity.MIN_DASH_DURATION or not self.dash_direction.y:
            self.entity.velocity.y = calculate_y_velocity(self.entity)
        else:
            self.entity.grounded = False
            self.entity.can_jump = False
            self.entity.air_timer += dt
            self.entity.velocity.y = move_towards(
                self.entity.INIT_JUMP_VELOCITY * self.entity.DASH_DURATION * self.entity.DASH_POWER,
                pow(abs(self.entity.velocity.y),
                    self.entity.DASH_POWER) * self.dash_direction.y,
                self.entity.DASH_ACCEL / TARGET_FPS)


class JUMP:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        if self.entity.events["dash"] and self.entity.can_dash:
            return DASH(self.entity, self.entity.direction)

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
        if self.entity.events["dash"] and self.entity.can_dash:
            return DASH(self.entity, self.entity.direction)

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
