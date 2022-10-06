from time import perf_counter

from pygame.time import Clock

from constants import FPS


class Engine:
    """
    Provides an interface to access the time between the last frame
    """
    def __init__(self):
        self.clock = Clock()
        self.t1 = perf_counter()

    def update(self):
        self.clock.tick(FPS)
        self.dt = (perf_counter() - self.t1)
        self.t1 = perf_counter()
