import pygame
import sys
import os
from pygame.locals import K_RETURN, K_ESCAPE, KEYDOWN
from Scripts.scene_manager import SceneManager
from Scenes.Levels.level_dependancies import Level

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
        self.lives = 3
        self.states = {
            "main_menu": MainMenuState(self, screen),
            "in_game": InGameState(self, screen),
            "pause": PauseState(self, screen),
            "game_over": GameOverState(self, screen),
        }
        self.current_state = self.states["main_menu"]

    def change_state(self, new_state_name):
        self.current_state = self.states[new_state_name]

    def start_new_game(self):
        self.lives = 3
        self.states["in_game"].scene_manager.restart()
        self.change_state("in_game")

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.change_state("game_over")
        else:
            self.states["in_game"].scene_manager.respawn_player()

    def handle_events(self, events):
        self.current_state.handle_events(events)

    def update_logic(self, events):
        self.current_state.update_logic(events)

    def update_graphics(self):
        self.current_state.update_graphics()

# --- Main Menu State ---
class MainMenuState(GameState):
    INTRO_DURATION = 180  # 3 seconds at 60fps

    def __init__(self, manager, screen):
        super().__init__(manager, screen)
        self.title_frames = self.load_title_frames("Assets/Universal/UI/TitleScreen")
        self.current_frame = 0
        self.frame_timer = 0

        self.intro_images = [
            pygame.image.load("Assets/Universal/UI/TitleScreen/Umar Ahmad.png").convert_alpha(),
            pygame.image.load("Assets/Universal/UI/TitleScreen/Presenting.png").convert_alpha(),
        ]
        self.intro_index = 0
        self.intro_timer = 0
        self.intro_done = False

    def load_title_frames(self, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.startswith("frame") and filename.endswith(".png"):
                path = os.path.join(folder_path, filename)
                frames.append(pygame.image.load(path).convert_alpha())
        return frames

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_RETURN and self.intro_done:
                    self.manager.start_new_game()

    def update_logic(self, events):
        pass

    def update_graphics(self):
        if not self.intro_done:
            self.update_intro()
            return

        title_screen = self.title_frames[self.current_frame]
        self.screen.blit(title_screen, (0, 0))  # Draw it to the screen
        self.frame_timer += 1
        if self.frame_timer >= 3:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.title_frames)

    def update_intro(self):
        self.screen.blit(self.intro_images[self.intro_index], (0, 0))
        self.intro_timer += 1
        if self.intro_timer >= self.INTRO_DURATION:
            self.intro_timer = 0
            self.intro_index += 1
            if self.intro_index >= len(self.intro_images):
                self.intro_done = True

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
        if self.scene_manager.player.is_dead:
            self.manager.lose_life()

    def update_graphics(self):
        self.scene_manager.update_graphics()
        if isinstance(self.scene_manager.current_scene, Level):
            lives_text = pygame.font.Font(None, 36).render(
                f"Lives: {self.manager.lives}", True, (255, 255, 255)
            )
            self.screen.blit(lives_text, (20, 20))

# --- Pause State ---
class PauseState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_state("in_game")
                elif event.key == pygame.K_q:
                    self.manager.change_state("main_menu")

    def update_logic(self, events):
        pass

    def update_graphics(self):
        in_game_state = self.manager.states["in_game"]
        in_game_state.update_graphics()

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        title_font = pygame.font.Font(None, 88)
        option_font = pygame.font.Font(None, 42)
        title = title_font.render("PAUSED", True, (255, 255, 255))
        resume = option_font.render("ESC  Resume", True, (255, 255, 255))
        menu = option_font.render("Q  Main Menu", True, (255, 255, 255))

        center_x = self.screen.get_width() // 2
        self.screen.blit(title, title.get_rect(center=(center_x, 250)))
        self.screen.blit(resume, resume.get_rect(center=(center_x, 360)))
        self.screen.blit(menu, menu.get_rect(center=(center_x, 420)))

# --- Game Over State ---
class GameOverState(GameState):
    def __init__(self, manager, screen):
        super().__init__(manager, screen)
        self.image = pygame.image.load("Assets/Universal/UI/End/gameover.png").convert_alpha()

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_RETURN:
                self.manager.change_state("main_menu")

    def update_logic(self, events):
        pass

    def update_graphics(self):
        self.screen.blit(self.image, (0, 0))

