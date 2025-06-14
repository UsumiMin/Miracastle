import pygame
from utils.animation import AnimationManager
from utils.collisions import handle_collisions
from settings import *
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animator = AnimationManager("player", scale=2)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.width = self.rect.width * 0.6
        self.rect_offset_x = 14
        self.rect.x += self.rect_offset_x
        self.facing_right = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_FORCE
        self.on_ground = False
        self.health = 100
        self.is_alive = True

    def set_player_state(self, base_state):
        state = base_state
        if not self.facing_right:
            state += "_flip"
        self.animator.set_state(state)
        return state
        

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.on_ground:
                self.velocity_y = -self.jump_power
                self.on_ground = False

    def update(self, platforms, camera):
        if not self.is_alive:
            return
        self.image = self.animator.update()
        old_x, old_y = self.rect.x, self.rect.y
        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, 15)
        safe_platforms = [p for p in platforms if not p.get('is_deadly', False)]
        self.rect.x, self.rect.y = handle_collisions(self, safe_platforms, camera, self.velocity_x, self.velocity_y, old_x, old_y)
        for platform in platforms:
            if 'is_deadly' in platform and platform['is_deadly'] and self.rect.colliderect(platform['rect']):
                self.respawn()
        if self.velocity_y < 0:
            self.set_player_state("jump")
        elif self.velocity_y > 0:
            self.set_player_state("fall")
        else:
            self.set_player_state("idle" if self.velocity_x == 0 else "run")


    def draw(self, screen, camera=None):
        if not self.is_alive:
            return
        pos = camera.apply(self.rect).topleft if camera else self.rect.topleft
        adjusted_pos = (pos[0] - self.rect_offset_x, pos[1])
        screen.blit(self.image, adjusted_pos)
    
    def respawn(self, x=INIT_X, y=INIT_Y):
        self.rect.topleft = (x, y)
        original_width = self.image.get_width()
        new_width = int(original_width * 0.6)
        self.rect.width = new_width
        self.rect_offset_x = 14
        self.rect.x += self.rect_offset_x
        self.health = 100
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.set_player_state("idle")