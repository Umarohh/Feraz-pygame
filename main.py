import pygame
import sys
from Scripts.game_state import GameStateManager

#Constants

FPS = 60

#Initialize Pygame
pygame.init()
# Get the screen resolution of the user's monitor
screen_width, screen_height = 1280, 720

# Create the screen in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Feraz")
clock = pygame.time.Clock()
gsm = GameStateManager(screen)

#Main Function, game loop calling the main class, update, and draw functions
def main():
    running = True
    #Handle Events
    while running:
        events = pygame.event.get()  # Get events here
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        gsm.handle_events(events)
        gsm.update_logic(events)
        screen.fill((0, 0, 0))
        gsm.update_graphics()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()   
    sys.exit()
    
if __name__ == "__main__":
    main()