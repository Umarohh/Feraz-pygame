import pygame


class Cutscene1:
    DURATION = 300  # 5 seconds at 60fps

    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("Assets/Cutscenes/cutscene1placeholder.png").convert_alpha()
        self.timer = 0
        self.completed = False

    def on_enter(self):
        """Prepare this cutscene when it becomes the active scene."""
        self.timer = 0
        self.completed = False

    def update(self, events):
        self.timer += 1
        if self.timer >= self.DURATION:
            self.completed = True

    def draw(self):
        self.screen.blit(self.image, (0, 0))
