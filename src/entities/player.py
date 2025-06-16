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
        self.rect.width = self.rect.width * CHAR_HIT
        self.rect_offset_x = 16
        self.rect.x += self.rect_offset_x
        self.facing_right = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_FORCE
        self.on_ground = False
        self.health = 100
        self.is_alive = True
        self.near_door = False

    def set_player_state(self, base_state):
        state = base_state + "_flip" if not self.facing_right else base_state
        self.animator.set_state(state)
        return state

    def _handle_movement_keys(self, keys):
        """Обработает движение игрока по клавишам."""
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True

    def _handle_jump_event(self, events):
        """Обрабатывает событие прыжка."""
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.on_ground:
                self.velocity_y = -self.jump_power
                self.on_ground = False
                return True
        return False

    def _handle_door_event(self, events):
        """Обрабатывает взаимодействие с дверью."""
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.near_door:
                return "change_level"
        return None       

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self._handle_movement_keys(keys)
        self._handle_jump_event(events)
        return self._handle_door_event(events)


    def update(self, platforms, camera, door_rect):
        if not self.is_alive:
            return

        # Обновление физики
        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, 15)
        old_x, old_y = self.rect.x, self.rect.y

        # Обработка столкновений
        safe_platforms = [p for p in platforms if not p.get('is_deadly', False)]
        self.rect.x, self.rect.y = handle_collisions(self, safe_platforms, camera, self.velocity_x, self.velocity_y, old_x, old_y)

        # Проверка смертельных платформ
        for platform in platforms:
            if platform.get('is_deadly', False) and self.rect.colliderect(platform['rect']):
                self.is_alive = False
                return

        # Проверка двери
        if door_rect and self.rect.colliderect(door_rect):
            self.near_door = True
        else:
            self.near_door = False

        # Установка состояния анимации
        if self.velocity_y < 0:
            self.set_player_state("jump")
        elif self.velocity_y > 0:
            self.set_player_state("fall")
        else:
            self.set_player_state("idle" if self.velocity_x == 0 else "run")

        self.image = self.animator.update()

    def draw(self, screen, camera=None):
        if not self.is_alive:
            return
        pos = camera.apply(self.rect).topleft if camera else self.rect.topleft
        adjusted_pos = (pos[0] - self.rect_offset_x, pos[1])
        screen.blit(self.image, adjusted_pos)
    
    def respawn(self, x=INIT_X, y=INIT_Y):
        self.rect.topleft = (x, y)
        original_width = self.image.get_width()
        new_width = int(original_width * CHAR_HIT)
        self.rect.width = new_width
        self.rect_offset_x = 16
        self.rect.x += self.rect_offset_x
        self.health = 100
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.set_player_state("idle")