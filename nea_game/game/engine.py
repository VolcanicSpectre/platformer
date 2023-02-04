from time import perf_counter

from pygame.time import Clock


class Engine:
    """
    Provides an interface to access the time difference between the when the previous frame that was drawn and the current frame was drawn
    """

    clock: Clock
    previous_time: float
    delta_time: float
    fps: int

    def __init__(self, fps: int):
        self.clock = Clock()
        self.previous_time = perf_counter()
        self.delta_time = 0
        self.fps = fps

    def update(self):
        """Limits the time between frames to the fps set at initialisation and updates delta_time to the time between the previous call"""
        self.clock.tick(self.fps)
        self.delta_time = perf_counter() - self.previous_time
        self.previous_time = perf_counter()
