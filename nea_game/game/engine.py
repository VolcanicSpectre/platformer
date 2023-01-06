from time import perf_counter

from pygame.time import Clock


class Engine:
    """
    Provides an interface to access the time between the last frame
    """

    def __init__(self, fps: int):
        self.clock = Clock()
        self.t1 = perf_counter()
        self.fps = fps

    def update(self):
        self.clock.tick(self.fps)
        self.dt = perf_counter() - self.t1
        self.t1 = perf_counter()
