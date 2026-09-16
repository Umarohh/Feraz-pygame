import pygame
from Scenes.Levels.level_1 import Level1  # Import level 1 class from file
from Scenes.Levels.level_2 import Level2  # Import level 2 class from file
from Scenes.Levels.level_3 import Level3  # Import level 3 class from file
from Scenes.Cutscenes.cutscene_1 import Cutscene1  # Import Cutscene 1 class from file
from Scenes.Cutscenes.cutscene_2 import Cutscene2  # Import Cutscene 2 class from file
from Scenes.Cutscenes.cutscene_3 import Cutscene3  # Import Cutscene 3 class from file
from Scripts.camera import Camera
from Scripts.player import Player

class SceneManager:
    """Class to manage the order and updating of levels of the game"""
    def __init__(self, screen):
        self.screen = screen
        self.camera = Camera(*screen.get_size()) # Create a camera object
        self.player = Player(0, 0)
        self.scenes = [Cutscene1(self.screen), Level1(self.screen, self.camera, self.player), Level2(self.screen, self.camera, self.player), Cutscene2(self.screen), Level3(self.screen, self.camera, self.player), Cutscene3(self.screen)]  # Chronological order of levels
        self.current_scene_index = 0  # Start at Cutscene 1
        self.current_scene = self.scenes[self.current_scene_index]  # The scene is the currently indexed scene
        self.current_scene.on_enter()

    def load_next_scene(self):
        """Advance to the next level if available"""
        if self.current_scene_index < len(self.scenes) - 1: # If there is a next level
            self.current_scene_index += 1 # Increment the level number in the index
            self.current_scene = self.scenes[self.current_scene_index] # The current level is the currently indexed level
            if hasattr(self.current_scene, "on_enter"):
                self.current_scene.on_enter()

    def respawn_player(self):
        """Reset the player at the current scene's starting position."""
        if hasattr(self.current_scene, "reset_player_and_camera"):
            self.current_scene.reset_player_and_camera()

    def restart(self):
        """Start the scene sequence again from cutscene 1."""
        self.current_scene_index = 0
        self.current_scene = self.scenes[self.current_scene_index]
        self.current_scene.on_enter()



    def update_logic (self, events):  
        """In game update logic"""

        if hasattr(self.current_scene, "update"):
            self.current_scene.update(events)
        if getattr(self.current_scene, "completed", False):
            self.load_next_scene() # If the current level is completed, load the next level

    



    def update_graphics(self): 
        """In game rendering logic"""
        if hasattr(self.current_scene, "draw"):
            self.current_scene.draw()

