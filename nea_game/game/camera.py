from pygame import Rect


class Camera:
    def __init__(
        self,
        height: int,
        width: int,
        surface_height: int,
        surface_width: int,
    ):
        self.height = height
        self.width = width

        self.surface_height = surface_height
        self.surface_width = surface_width

        self.scroll_x: int = 0
        self.scroll_y: int = 0

        self.trauma: float = 0

    def update(self, target_rect: Rect):
        """Updates the scroll values of the camera to focus on the target

        Args:
            target_rect (Rect): The rect for a given target
        """
        self.scroll_x += int(
            (
                target_rect.x
                - self.scroll_x
                - (self.surface_width + target_rect.width) // 2
            )
            * 0.2
        )

        self.scroll_y += int(
            (
                target_rect.y
                - self.scroll_y
                - (self.surface_height + target_rect.height) // 2
            )
            * 0.2
        )

        self.scroll_x = min(max(0, self.scroll_x), self.width - self.surface_width)
        self.scroll_y = min(max(0, self.scroll_y), self.height - self.surface_height)
