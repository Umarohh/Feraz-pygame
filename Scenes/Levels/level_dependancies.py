import os
import pygame
from Scripts.tile import Tile, Tilemap

class Level:
    spawn_position = (0, 0)

    def __init__(self, screen, camera, player, level_name=None):
        """Initialize the parent level class"""
        self.screen = screen
        self.completed = False  # Track if the level is completed
        self.camera = camera
        self.player = player
        self.bg_layers = []
        self.bg_layer_speeds = [0.003, 0.007, 0.009, 0.08, 0.2]
        self.bg_layer_widths = []
        self.tilemap = None

        if level_name is not None:
            self.load_level_assets(level_name)



    def check_completion_condition(self): # Ensures all levels have a completion condition regardless of specific update method
        return False
       
    def is_completed(self):
        """Return whether the level is completed to outside classes such as level_manager"""
        return self.completed
    
    def update(self, events):
        """Update level logic and shared player/camera state."""
        self.update_logic()
        if self.check_completion_condition():
            self.completed = True
        if self.tilemap is not None:
            self.tilemap.update()
            self.player.update(events, self.tilemap.tiles)
            self.camera.update(self.player)

    def draw(self):
        """Render level content and the shared player."""
        self.render_parallax(self.screen, self.camera.camera.x)
        if self.tilemap is not None:
            self.tilemap.render(self.screen, self.camera)
        self.player.render(self.screen, self.camera)

    def load_level_assets(self, level_name):
        """Load a level map and all PNG backgrounds from its asset folder."""
        level_path = os.path.join("Assets", "Levels", level_name)
        map_path = next(
            os.path.join(level_path, "Map", filename)
            for filename in os.listdir(os.path.join(level_path, "Map"))
            if filename.endswith(".txt")
        )

        Tile.load_tile_images()
        self.tilemap = Tilemap()
        self.tilemap.load_from_file(map_path)

        self.reset_player_and_camera()

    def reset_player_and_camera(self):
        """Reset shared gameplay state for this level."""
        if self.tilemap is None:
            return
        self.camera.set_level_bounds(self.tilemap.pixel_width, self.tilemap.pixel_height)
        self.player.set_level_bounds(self.tilemap.pixel_width, self.tilemap.pixel_height)
        self.player.reset_position(*self.spawn_position)
        self.camera.reset(self.player)

    def on_enter(self):
        """Prepare this level when it becomes the active scene."""
        self.reset_player_and_camera()

    def load_backgrounds(self, *bg_paths):
        """Load background images for all layers and track their widths"""
        for path in bg_paths:
            bg = pygame.image.load(path).convert_alpha()
            self.bg_layers.append(bg)
            self.bg_layer_widths.append(bg.get_width())

    def render_parallax(self, screen, camera_x):
        """Render parallax layers based on the camera position"""
        for i, bg in enumerate(self.bg_layers):
            speed = self.bg_layer_speeds[i]  # Speed for this specific layer
            width = self.bg_layer_widths[i]  # Width of the current background layer

            # Calculate the x position of the layer with scrolling effect
            scroll_x = -camera_x * speed
            start_x = int(scroll_x) % width  # Wrapping point for seamless cycling

            # Draw the backgrounds in a loop, covering the screen seamlessly
            for offset in (-1, 0, 1):
                x = start_x + offset * width
                screen.blit(bg, (x, 0))  # Draw the background at the calculated position
