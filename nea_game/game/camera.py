from pygame import Rect


class Camera:
    """
    Provides a camera class that can adjust the scroll values on both axis in order to focus and move to smoothly a specific pygame.Rect
    """

    height: int
    width: int
    display_surface_height: int
    display_surface_width: int
    scroll_x: int
    scroll_y: int
    trauma: float

    def __init__(
        self,
        height: int,
        width: int,
        display_surface_height: int,
        display_surface_width: int,
    ):
        self.height = height
        self.width = width

        self.display_surface_height = display_surface_height
        self.display_surface_width = display_surface_width

        self.scroll_x = 0
        self.scroll_y = 0

        self.trauma = 0

    def update(self, target_rect: Rect):
        """Updates the scroll values of the camera to focus on the target

        Args:
            target_rect (Rect): The rect for a given target
        """
        self.scroll_x += int(
            (
                target_rect.x
                - self.scroll_x
                - (self.display_surface_width + target_rect.width) // 2
            )
            * 0.2
        )

        self.scroll_y += int(
            (
                target_rect.y
                - self.scroll_y
                - (self.display_surface_height + target_rect.height) // 2
            )
            * 0.2
        )

        self.scroll_x = min(
            max(0, self.scroll_x), self.width - self.display_surface_width
        )
        self.scroll_y = min(
            max(0, self.scroll_y), self.height - self.display_surface_height
        )
