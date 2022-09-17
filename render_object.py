from numba.experimental import jitclass
from numba import int32, float32
from numpy import array, dtype


@jitclass
class RenderObject:
    x: int
    y: int
    image:array(int32, 2d, C)
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
