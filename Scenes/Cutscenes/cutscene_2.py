import pygame

class Cutscene2:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("Assets/Universal/UI/End/end card.png").convert_alpha()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self):
        self.screen.blit(self.image, (0, 0))

