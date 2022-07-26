from functools import partial
from math import copysign

sign = partial(copysign, 1)


class IDLE:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        if self.entity.direction:
            return RUN(self.entity)

        if self.entity.events["up"] and self.entity.air_timer == 0:
            return JUMP(self.entity)

        return self

    def process_x_movement(self, dt):
        return self

    def process_y_movement(self, dt):
        if self.entity.air_timer or not self.entity.grounded:
            return FALL(self.entity)

        return self


class RUN:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        if self.entity.events["up"] and self.entity.air_timer == 0:
            return JUMP(self.entity)

        if self.entity.velocity.x == 0 and not self.entity.direction:
            return IDLE(self.entity)

        return self
        # TODO add dash

    def process_x_movement(self, dt):
        if self.entity.velocity.x == 0 and not self.entity.direction:
            return IDLE(self.entity)

        self.entity.velocity.x = calculate_x_velocity(self.entity)
        return self

    def process_y_movement(self, dt):
        if self.entity.air_timer or not self.entity.grounded:
            return FALL(self.entity)

        return self


class DASH(RUN):
    DASHTIME = 0.4

    def __iter__(self):
        yield DASH.DASHTIME


class JUMP:
    def __init__(self, entity):
        self.entity = entity
        print(min(self.entity.y_heights))
        self.entity.y_heights = []

    def process_y_movement(self, dt):
        self.entity.velocity.y = self.entity.INIT_JUMP_VELOCITY
        self.entity.air_timer += dt
        return FALL(self.entity)

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity)

        return self


class FALL:
    def __init__(self, entity):
        self.entity = entity

    def input_handler(self):
        return self

    def process_y_movement(self, dt):
        if self.entity.velocity.y < 0:
            self.entity.velocity.y += self.entity.INIT_GRAVITY
        else:
            self.entity.velocity.y += self.entity.FINAL_GRAVITY

        if not self.entity.air_timer and self.entity.grounded:
            if self.entity.velocity.x == 0 and not self.entity.direction:
                return IDLE(self.entity)
            else:
                return RUN(self.entity)

        self.entity.air_timer += dt
        return self

    def process_x_movement(self, dt):
        self.entity.velocity.x = calculate_x_velocity(self.entity)

        return self


def calculate_x_velocity(entity):
    target_velocity = entity.MAXRUN * entity.direction
    if abs(target_velocity) < 0.01:
        vel_power = entity.STOPPOWER
    elif abs(entity.velocity.x) > 0 and sign(target_velocity) != sign(entity.velocity.x):
        vel_power = entity.TURNPOWER
    else:
        vel_power = entity.ACCELPOWER

    accel_rate = pow((entity.ACCELRUN * 1 / 60), vel_power)
    return move_towards(entity.velocity.x, target_velocity, accel_rate)


def move_towards(current, target, max_delta):
    if current > target:
        return max(current - max_delta, target)
    else:
        return min(current + max_delta, target)

# TODO multiply the whole y velo by dtg
