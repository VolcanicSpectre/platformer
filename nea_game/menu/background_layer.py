from math import sin
from time import perf_counter
from random import uniform
from pygame import Rect, Surface


class BackgroundLayer:
    image: Surface
    sine_scale_factor: float
    sine_stretch_factor: float
    sine_translation_factor: float
    x_scroll: float

    def __init__(self, image: Surface):
        self.image = image

        self.sine_scale_factor = uniform(0.001, 0.1)
        self.sine_stretch_factor = pow(10, 20)
        self.sine_translation_factor = uniform(0.1, 0.7)

        self.x_scroll = 0

    def get_new_sub_image(self, x_scroll: float = 0, y_scroll: float = 0) -> Surface:
        """Generates a new scroll value to adjust which subsection of the image is returned

        Returns:
            Surface: The sub image according to the newly generated scroll value
        """
        self.x_scroll += (
            self.sine_scale_factor * abs(sin(perf_counter() * self.sine_stretch_factor))
            + self.sine_translation_factor
        ) + x_scroll

        x_scroll = int(self.x_scroll) % (self.image.get_width() // 2)

        handle_image = self.image.copy()
        clip_rect = Rect(
            x_scroll, y_scroll, self.image.get_width() // 2, self.image.get_height()
        )
        handle_image.set_clip(clip_rect)
        return self.image.subsurface(handle_image.get_clip())
