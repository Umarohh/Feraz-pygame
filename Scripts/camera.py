import pygame


class Camera:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)
        self.camera_pos = pygame.Vector2(0, 0)
        self.level_width = width
        self.level_height = height

        self.smoothness = 0.08
        self.look_ahead = 110      # keeps more of the level visible ahead of the player
        self.top_margin = 150      # vertical dead zone: camera only moves when the
        self.bottom_margin = 200   # player leaves this band

    def set_level_bounds(self, width, height):
        self.level_width = width
        self.level_height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def apply_to_rect(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)

    def apply_to_point(self, point):
        return pygame.Vector2(point) - pygame.Vector2(self.camera.topleft)

    def reset(self, target):
        """Snap the camera onto the target instead of smoothing toward it."""
        rect = target.rect
        self.camera_pos.update(
            rect.centerx - self.width // 2 + self.look_ahead,
            rect.centery - self.height // 2,
        )
        self._clamp_and_apply()

    def update(self, target):
        rect = target.rect

        desired_x = rect.centerx - self.width // 2 + self.look_ahead
        self.camera_pos.x += (desired_x - self.camera_pos.x) * self.smoothness

        band_top = self.camera_pos.y + self.top_margin
        band_bottom = self.camera_pos.y + self.height - self.bottom_margin
        if rect.top < band_top:
            desired_y = rect.top - self.top_margin
            self.camera_pos.y += (desired_y - self.camera_pos.y) * self.smoothness
        elif rect.bottom > band_bottom:
            desired_y = rect.bottom - self.height + self.bottom_margin
            self.camera_pos.y += (desired_y - self.camera_pos.y) * self.smoothness * 3

        self._clamp_and_apply()

    def _clamp_and_apply(self):
        max_x = max(0, self.level_width - self.width)
        max_y = max(0, self.level_height - self.height)
        self.camera_pos.x = max(0, min(self.camera_pos.x, max_x))
        self.camera_pos.y = max(0, min(self.camera_pos.y, max_y))
        self.camera.topleft = (round(self.camera_pos.x), round(self.camera_pos.y))
