from pygame.time import Clock
from time import perf_counter

class Engine:
    def __init__(self):
        self.clock = Clock()
        self.t1 = perf_counter()
    
    def update_dt(self):
        self.dt = perf_counter() - self.t1
        self.t1 = perf_counter()
    