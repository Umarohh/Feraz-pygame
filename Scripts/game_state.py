import pygame
import sys
from pygame.locals import K_RETURN, K_ESCAPE, KEYDOWN
from Scripts.scene_manager import SceneManager

# --- Parent GameState class ---
class GameState:
    def __init__(self, manager, screen):
        self.manager = manager
        self.screen = screen

    def handle_events(self, events):
        for event in events:
            pass
    def update_logic(self): pass
    def update_graphics(self): pass

# --- Game State Manager ---
class GameStateManager:
    def __init__(self, screen):
        self.screen = screen
        self.states = {
            "main_menu": MainMenuState(self, screen),
            "in_game": InGameState(self, screen),
            "pause": PauseState(self, screen),
            "game_over": GameOverState(self, screen),
        }
        self.current_state = self.states["main_menu"]

    def change_state(self, new_state_name):
        self.current_state = self.states[new_state_name]

    def handle_events(self, events):
        self.current_state.handle_events(events)

    def update_logic(self, events):
        self.current_state.update_logic(events)

    def update_graphics(self):
        self.current_state.update_graphics()

# --- Main Menu State ---
class MainMenuState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.manager.change_state("in_game")

    def update_logic(self, events):
        pass

    def update_graphics(self):
        title_screen = pygame.image.load("Assets/Universal/UI/title_screen.jpeg")
        self.screen.blit(title_screen, (0, 0))  # Draw it to the screen
        
# --- In Game State ---
class InGameState(GameState):
    def __init__(self, manager, screen):
        super().__init__(manager, screen)
        self.scene_manager = SceneManager(screen)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state("pause")

    def update_logic(self, events):
        self.scene_manager.update_logic(events)

    def update_graphics(self):
        self.scene_manager.update_graphics()

# --- Pause State ---
class PauseState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state("in_game")
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()

    def update_logic(self, events):
        pass

    def update_graphics(self):
        pass

# --- Game Over State ---
class GameOverState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_RETURN:
                self.manager.change_state("main_menu")

    def update_logic(self, events):
        pass

    def update_graphics(self):
        pass

