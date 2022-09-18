from numba import int32
from numba.experimental import jitclass


@jitclass
class RenderObject:
    x: int
    y: int
    image: int32[:, :]

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
