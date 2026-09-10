import pygame
from Scenes.Levels.level_dependancies import Level

class Level1(Level):
    def __init__(self, screen, camera, player):
        super().__init__(screen, camera, player, "Level1")
        self.load_backgrounds(
            "Assets/Levels/Level1/Background/sky_moon.png",
            "Assets/Levels/Level1/Background/clouds.png",
            "Assets/Levels/Level1/Background/back_trees.png",
            "Assets/Levels/Level1/Background/middle_trees.png",
            "Assets/Levels/Level1/Background/front_trees.png",
        )


    def update_logic(self):
        pass
    


    def check_completion_condition(self):
        """Return whether the level is completed."""
        if self.player.rect.x > 4515:
            print("Level 1 completed!")
            return True

        