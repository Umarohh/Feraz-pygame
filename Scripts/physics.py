import pygame 

class PhysicsObject(pygame.sprite.Sprite):
    def __init__(self, x, y, gravity=0.5):
        super().__init__()
        self.x_velocity = 0
        self.y_velocity = 0
        self.gravity = gravity
        self.max_fall_speed = 10  # Define max fall speed
        self.is_on_ground = False
        self.colliding_left = False
        self.colliding_right = False

    def handle_gravity(self):
        if not self.is_on_ground:  # Only apply gravity if not on the ground
            self.y_velocity += self.gravity
            if self.y_velocity > self.max_fall_speed:  # Max fall speed
                self.y_velocity = self.max_fall_speed

    def handle_collisions(self, tiles):
        self.colliding_left = False
        self.colliding_right = False

        epsilon = 1  # small margin for adjacency

        # Horizontal movement
        self.rect.x += self.x_velocity

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.x_velocity > 0:
                    self.rect.right = tile.rect.left
                    self.x_velocity = 0
                    self.colliding_right = True
                elif self.x_velocity < 0:
                    self.rect.left = tile.rect.right
                    self.x_velocity = 0
                    self.colliding_left = True

        for tile in tiles:
            if self.rect.bottom > tile.rect.top and self.rect.top < tile.rect.bottom:
                if 0 <= self.rect.left - tile.rect.right <= epsilon:
                    self.colliding_left = True
                if 0 <= tile.rect.left - self.rect.right <= epsilon:
                    self.colliding_right = True

        # Vertical movement
        self.rect.y += self.y_velocity
        self.is_on_ground = False

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.y_velocity > 0:
                    self.rect.bottom = tile.rect.top
                    self.y_velocity = 0
                    self.is_on_ground = True
                    self.jumps_left = self.max_jumps
                elif self.y_velocity < 0:
                    self.rect.top = tile.rect.bottom
                    self.y_velocity = 0

        # Resting-contact check: catches standing exactly on a tile with
        # zero overlap, so is_on_ground doesn't flicker False when y_velocity is 0
        if not self.is_on_ground:
            for tile in tiles:
                horizontally_aligned = self.rect.right > tile.rect.left and self.rect.left < tile.rect.right
                resting_on_top = 0 <= tile.rect.top - self.rect.bottom <= epsilon
                if horizontally_aligned and resting_on_top:
                    self.is_on_ground = True
                    self.jumps_left = self.max_jumps
                    break