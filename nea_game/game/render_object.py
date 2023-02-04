from pygame import Surface


class RenderObject:
    x: int
    y: int
    image: Surface

    def __init__(self, x: int, y: int, image: Surface):
        self.x = x
        self.y = y
        self.image = image
