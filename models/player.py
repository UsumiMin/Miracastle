import pygame
from utils.animation import AnimationManager
from utils.collisions import handle_collisions
from settings import *
from utils.audio import AudioManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.animator = AnimationManager("player", scale=2)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.width = self.rect.width * PLAYER_HIT
        self.rect_offset_x = PLAYER_OFFSET
        self.rect.x += self.rect_offset_x
        self.facing_right = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_FORCE
        self.on_ground = True
        self.health = PLAYER_HEALTH
        self.is_alive = True
        self.near_door = False
        self.step_timer = 0
        self.step_interval = PLAYER_STEP_INTER
        self.last_step_time = pygame.time.get_ticks()
        self.audio = AudioManager()

    def update_physics(self, platforms):
        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, 15)
        old_x, old_y = self.rect.x, self.rect.y
        safe_platforms = [p for p in platforms if not p.get('is_deadly', False)]
        self.rect.x, self.rect.y = handle_collisions(self, safe_platforms, self.velocity_x, self.velocity_y, old_y)

        for platform in platforms:
            if platform.get('is_deadly', False) and self.rect.colliderect(platform['rect']):
                self.is_alive = False
                return
        self.on_ground = any(self.rect.bottom == p['rect'].top and self.velocity_y >= 0 for p in safe_platforms)
            
    def update_state(self, door_rect=None):
        if door_rect and self.rect.colliderect(door_rect):
            self.near_door = True
        else:
            self.near_door = False
        if self.health <= 0:
            self.is_alive = False

    def set_state(self, base_state):
        state = base_state + "_flip" if not self.facing_right else base_state
        self.animator.set_state(state)
        return state

    def respawn(self, x=INIT_X, y=INIT_Y):
        self.rect.topleft = (x, y)
        original_width = self.image.get_width()
        new_width = int(original_width * PLAYER_HIT)
        self.rect.width = new_width
        self.rect_offset_x = PLAYER_OFFSET
        self.rect.x += self.rect_offset_x
        self.health = PLAYER_HEALTH
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.set_state("idle")