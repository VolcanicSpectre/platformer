from pygame import Surface


class RenderObject:
    x: int
    y: int
    image: Surface

    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
