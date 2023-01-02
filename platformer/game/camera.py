from pygame import Rect


class Camera:
    def __init__(
        self,
        height: int,
        width: int,
        surface_height: int,
        surface_width: int,
        unit_length: int = 1,
    ):
        self.height = height
        self.width = width

        self.surface_height = surface_height
        self.surface_width = surface_width

        self.unit_length = unit_length

        self.true_scroll_x: float = 0
        self.true_scroll_y: float = 0
        self.scroll_x: int = 0
        self.scroll_y: int = 0

    def update(self, target_rect: Rect):
        """Updates the scroll values of the camera to focus on the target

        Args:
            target_rect (Rect): The rect for a given target
        """
        if (
            0
            <= self.true_scroll_x
            <= (self.width - self.surface_width + self.unit_length)
        ):
            self.scroll_x = int(self.true_scroll_x)

        if (
            0
            <= self.true_scroll_y
            <= (self.height - self.surface_height + self.unit_length)
        ):
            self.scroll_y = int(self.true_scroll_y)

        self.true_scroll_x += (
            target_rect.centerx
            - self.true_scroll_x
            - (self.surface_width - target_rect.width + self.unit_length) // 2
        ) / 20
        self.true_scroll_y += (
            target_rect.centery
            - self.true_scroll_y
            - (self.surface_height - target_rect.height + self.unit_length) // 2
        ) / 20

    def get_scroll_x(self):
        return int(self.scroll_x)

    def get_scroll_y(self):
        return int(self.scroll_y)
