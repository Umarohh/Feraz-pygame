import pygame
import os
from Scripts.physics import PhysicsObject
from Scenes.Levels.level_1 import Level1

class Player(PhysicsObject, pygame.sprite.Sprite):
    def __init__(self, x, y):
        PhysicsObject.__init__(self, x, y, gravity=0.5)
        pygame.sprite.Sprite.__init__(self)
        '''Init Objects'''
        self.load_images()
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect().inflate(-35, -10)
        self.rect.center = (x, y)
        self.facing = "right"       
        self.current_frame = 0
        self.frame_timer = 0
        self.current_animation = "idle"
        self.sprint = False
        self.jump_force = 10
        self.jump_hold_time = 10
        self.jump_active = False
        self.jump_timer = 0
        self.max_jumps = 2
        self.jumps_left = self.max_jumps
        self.is_on_ground = False
        self.x_velocity = 0
        self.y_velocity = 0
        self.idle()

    def load_animation(self, folder_path):
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                path = os.path.join(folder_path, filename)
                image = pygame.image.load(path).convert_alpha()
                frames.append(image)
        return frames

    def load_images(self):
        self.idle_frames = self.load_animation("assets/universal/player/idle")
        self.walking_frames = self.load_animation("assets/universal/player/walking")
        self.running_frames = self.load_animation("assets/universal/player/running")
        self.sprinting_frames = self.load_animation("assets/universal/player/sprinting")
        self.jumping_frames = self.load_animation("assets/universal/player/jumping")
        self.jumping_facing_frames = self.load_animation("assets/universal/player/jumping_facing")
        self.falling_frames = self.load_animation("assets/universal/player/falling")
        self.falling_facing_frames = self.load_animation("assets/universal/player/falling_facing")

        self.animations = {
            "idle": self.idle_frames,
            "walk": self.walking_frames,
            "run": self.running_frames,
            "sprint": self.sprinting_frames,
            "jump": self.jumping_frames,
            "jump_direction": self.jumping_facing_frames,
            "fall": self.falling_frames,
            "fall_direction": self.falling_facing_frames,
        }

    def set_animation(self, name):
        if name != self.current_animation:
            self.current_animation = name
            self.current_frame = 0
            self.frame_timer = 0

        frame = self.animations[name][self.current_frame]
        if self.x_velocity < 0:
            self.image = pygame.transform.flip(frame, True, False)
        else:
            self.image = frame

    def update_animation(self):
        print(f"anim={self.current_animation} frame={self.current_frame} grounded={self.is_on_ground} vel=({self.x_velocity:.1f},{self.y_velocity:.1f})")

        self.frame_timer += 1
        if self.frame_timer > 5:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.animations[self.current_animation]):
                self.current_frame = 0

        frame = self.animations[self.current_animation][self.current_frame]
        if self.facing == "left":
            self.image = pygame.transform.flip(frame, True, False)
        else:
            self.image = frame

    def handle_input(self, events):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not self.colliding_left:
            self.move_left()
            self.facing = "left"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not self.colliding_right:
            self.move_right()
            self.facing = "right"
        else:
            self.idle()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if self.jumps_left > 0:
                        self.start_jump()

        self.sprint = keys[pygame.K_LSHIFT]

    def idle(self):
        if abs(self.x_velocity) < 1:
            self.x_velocity = 0
        elif self.x_velocity > 0:
            self.x_velocity -= .5
        elif self.x_velocity < 0:
            self.x_velocity += .5

    def move_left(self):
        if self.sprint:
            if (self.x_velocity) < -7.5:
                acceleration = -0.05
            elif (self.x_velocity) < -6:
                acceleration = -0.1
            else:
                acceleration = -.4
            max_speed = -8
        else:
            acceleration = -0.2
            max_speed = -4

        if self.x_velocity > max_speed:
            self.x_velocity += acceleration
        if self.x_velocity < max_speed:
            self.x_velocity = max_speed

    def move_right(self):
        if self.sprint:
            if (self.x_velocity) > 7.5:
                acceleration = 0.05
            elif (self.x_velocity) > 6:
                acceleration = 0.1
            else:
                acceleration = .4
            max_speed = 8
        else:
            acceleration = 0.2
            max_speed = 4

        if self.x_velocity < max_speed:
            self.x_velocity += acceleration
        if self.x_velocity > max_speed:
            self.x_velocity = max_speed

    def start_jump(self):
        self.jump_active = True
        self.jump_timer = self.jump_hold_time
        self.y_velocity = -self.jump_force
        self.jumps_left -= 1
        self.set_animation("jump")

    def continue_jump(self):
        if self.jump_timer > 0:
            self.y_velocity = -self.jump_force
            self.jump_timer -= 1
        else:
            self.jump_active = False

    def choose_movement_animations(self):
        
        if not self.is_on_ground:
            if self.y_velocity <= 0:
                self.set_animation("jump" if self.x_velocity != 0 else "jump_direction")
            else:
                self.set_animation("fall" if self.x_velocity != 0 else "fall_direction")
            return

        speed = abs(self.x_velocity)
        if speed == 0:
            self.set_animation("idle")
        elif speed >= 7:
            self.set_animation("sprint")
        elif speed >= 5:
            self.set_animation("run")
        else:  # covers every remaining case: 0 < speed < 5
            self.set_animation("walk")



    def render(self, screen, camera):
        offset_pos = self.rect.topleft + pygame.Vector2(-17, 0)
        screen.blit(self.image, camera.apply_to_point(offset_pos))


    def set_level_bounds(self, level_width, level_height): #not functional yet
        # Prevent going out of bounds horizontally
        if self.rect.left < 0:
            self.rect.left = 0
            self.x_velocity = 0
        elif self.rect.right > level_width:
            self.rect.right = level_width
            self.x_velocity = 0

        # Prevent going out of bounds vertically
        if self.rect.top < 0:
            self.rect.top = 0
            self.y_velocity = 0
        elif self.rect.bottom > level_height:
            self.rect.bottom = level_height
            self.y_velocity = 0
            self.is_on_ground = True
    

    def reset_position(self, x, y):
        self.x = x  # PhysicsObject x position
        self.y = y  # PhysicsObject y position
        self.rect.center = (x, y)  # Sprite rect position

        self.x_velocity = 0
        self.y_velocity = 0
        self.jumps_left = self.max_jumps
    
    def update(self, events, tiles):
        self.handle_input(events)

        keys = pygame.key.get_pressed()
        if self.jump_active and (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            self.continue_jump()
        else:
            self.jump_active = False
    
        self.handle_gravity()
        self.handle_collisions(tiles)
        self.choose_movement_animations()
        self.update_animation()
        
