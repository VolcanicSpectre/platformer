from math import sin
from time import perf_counter
from random import uniform
from pygame import Rect, Surface


class SplashScreenLayer:
    image: Surface
    sine_scale_factor: float
    sine_stretch_factor: float
    x_scroll: float

    def __init__(self, image: Surface):
        self.image = image
        self.sine_scale_factor = uniform(1.5, 2)
        print(self.sine_scale_factor)
        self.sine_stretch_factor = uniform(5, 8)

        self.x_scroll = 0

    def get_new_sub_image(self) -> Surface:
        """Generates a new scroll value to adjust which subsection of the image is returned

        Returns:
            Surface: The sub image according to the newly generated scroll value
        """
        self.x_scroll += self.sine_scale_factor * abs(sin(
            perf_counter() * self.sine_stretch_factor
        ))

        x_scroll = int(self.x_scroll) % (self.image.get_width() // 2)

        handle_image = self.image.copy()
        clip_rect = Rect(
            x_scroll, 0, self.image.get_width() // 2, self.image.get_height()
        )
        handle_image.set_clip(clip_rect)
        return self.image.subsurface(handle_image.get_clip())
