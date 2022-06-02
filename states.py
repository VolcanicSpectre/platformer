from enum import Enum
from math import copysign
from functools import partial

sign = partial(copysign, 1)


class NULL:
    def __init__(self, entity): self.entity = entity

    def input_handler(self): return NULL(self.entity)

    def process_x_movement(self, dt): return NULL(self.entity)

    def process_y_movement(self, dt): return NULL(self.entity)


class IDLE(NULL):
    def input_handler(self):
        if self.entity.direction:
            return RUN(self.entity)

        if self.entity.events["up"]:
            return JUMP(self.entity)

        return self

    def process_x_movement(self, dt):
        return self

    def process_y_movement(self, dt):
        self.entity.velocity.y += self.entity.FINAL_GRAVITY * dt

        if not self.entity.air_timer:
            return FALL(self.entity)

        return self


class RUN(NULL):
    def input_handler(self):
        if self.entity.events["up"]:
            return JUMP(self.entity)

        if not self.entity.direction:
            return IDLE(self.entity)

        return self
        # TODO add dash

    def process_x_movement(self, dt):

        if not self.entity.direction:
            return IDLE(self.entity)

        self.entity.velocity.x = calculate_x_velocity(self.entity, dt)

        return self

    def process_y_movement(self, dt):
        self.entity.velocity.y += self.entity.FINAL_GRAVITY * dt
        if not self.entity.air_timer:
            return FALL(self.entity)

        return self


class DASH(RUN):
    DASHTIME = 0.4

    def __iter__(self):
        yield DASH.DASHTIME


class JUMP(NULL):
    def input_handler(self):
        print(self)
        return self

    def proceess_y_movement(self, dt):
        self.entity.velocity.y += self.entity.INIT_GRAVITY * dt

        if not self.entity.air_timer:

            if self.entity.direction:
                return RUN(self.entity)

            else:
                return IDLE(self.entity)

        return self

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity, dt)
        return self


class FALL(NULL):
    def input_handler(self): return self

    def proceess_y_movement(self, dt):
        self.entity.velocity.y += self.entity.FINAL_GRAVITY * dt

        if self.entity.air_timer:
            if self.entity.entity.entity.direction:
                return RUN(self.entity)
            else:
                return IDLE(self.entity)

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity, dt)

        return self


def calculate_x_velocity(entity, dt):
    u = entity.velocity.x
    target_speed = entity.MAXRUN * entity.direction

    if abs(target_speed) > 0.01:
        a = entity.ACCELRUN
        if not entity.air_timer:
            a *= 0.01
    else:
        a = entity.DECELRUN
        if not entity.air_timer:
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

    if entity.direction > 0:
        return min(u + v, target_speed)
    if entity.direction < 0:
        return max(u + v*entity.x_move_input, target_speed)
    else:
        if sign(u) == -1:
            return min(u - (v*-1), target_speed*entity.direction)
        else:
            return max(u - v, target_speed*entity.direction)
