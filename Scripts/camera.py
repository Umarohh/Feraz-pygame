import pygame

class Camera:
    def __init__(self):
        self.width = 720
        self.height = 1280
        self.camera = pygame.Rect(0, 0, self.width, self.height)
        self.camera_pos = pygame.Vector2(0, 0)
        self.smoothness = 0.05
        self.level_width = 0
        self.level_height = 0

        self.top_margin = 100
        self.bottom_margin = 650

        self.target_base_y = None  # Keeps track of the target "base" y position

    def set_level_bounds(self, width, height):
        self.level_width = width
        self.level_height = height

    def apply(self, entity):
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def apply_to_rect(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)

    def apply_to_point(self, point):
        return pygame.Vector2(point) - pygame.Vector2(self.camera.topleft)

    def update(self, target):
        target_rect = target.rect

        # --- Horizontal Tracking ---
        desired_x = target_rect.centerx - self.width // 2 + 110 
        self.camera_pos.x += (desired_x - self.camera_pos.x) * self.smoothness
        self.camera_pos.x = max(0, min(self.camera_pos.x, self.level_width - 2 * self.width + 110))


        # --- Vertical Dead Zones ---
        screen_top = self.camera_pos.y + self.top_margin
        screen_bottom = self.camera_pos.y + self.height - self.bottom_margin

        # Move up if player jumps too high
        if target_rect.top < screen_top:
            desired_y = target_rect.top - self.top_margin
            self.camera_pos.y += (desired_y - self.camera_pos.y) * self.smoothness

            # Update the "base" Y to follow the player’s higher elevation
            self.target_base_y = self.camera_pos.y

        # Move down faster if player falls far below the screen
        elif target_rect.bottom > screen_bottom:
            desired_y = target_rect.bottom - self.height + self.bottom_margin
            self.camera_pos.y += (desired_y - self.camera_pos.y) * 5 * self.smoothness
            self.camera_pos.y = max(0, min(self.camera_pos.y, self.level_height - self.height))


            # Allow reset of the base camera position if player lands on lower ground
            self.target_base_y = self.camera_pos.y

        # If player is within vertical dead zone but camera is too high above current platform,
        # return gently to most recent valid "base" Y
  
        # --- Update the camera rectangle ---
        self.camera.topleft = (int(self.camera_pos.x), int(self.camera_pos.y))

