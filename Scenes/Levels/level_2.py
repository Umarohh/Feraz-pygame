import pygame
from Scenes.Levels.level_dependancies import Level

class Level2(Level):
    def __init__(self, screen, camera, player):
        super().__init__(screen, camera, player, "Level2")
        self.load_backgrounds(
            "Assets/Levels/Level2/Background/moonsky.png",
            "Assets/Levels/Level2/Background/cloud.png",
            "Assets/Levels/Level2/Background/hills.png",
            "Assets/Levels/Level2/Background/houses.png",
            "Assets/Levels/Level2/Background/fence.png",
        )



    def update_logic(self):
        """Level 2 logic"""
        pass
        


    def check_completion_condition(self):
        """Check if the level is completed"""
        # Placeholder for actual completion logic
        # For example, check if a certain condition is met in the game
        return False

 