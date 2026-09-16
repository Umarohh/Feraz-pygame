import pygame
from Scenes.Levels.level_dependancies import Level

class Level2(Level):
    spawn_position = (128, 3392)  # bottom-left of the tower
    FINISH_TOP = 12 * 32
    FINISH_LEFT = 42 * 32

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
        """Completed once the player is standing on the finish ledge at the top."""
        rect = self.player.rect
        return (
            self.player.is_on_ground
            and rect.bottom <= self.FINISH_TOP + 1
            and rect.centerx >= self.FINISH_LEFT
        )

 