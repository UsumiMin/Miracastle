import pygame
from utils.animation import AnimationManager
from utils.collisions import handle_collisions
from settings import *
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        sprite_path = os.path.join(ASSETS_PATH, "sprites", "characters", "player")
        states = {
            "idle": {"flip": True},
            "run": {"flip": True},  # Автоматически создаст run_flip
            "jump": {"flip": True}, 
            "fall": {"flip": True},
        }
        self.animator = AnimationManager(sprite_path, states, scale=2)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.width = self.rect.width * 0.6
        self.rect_offset_x = 14  # Смещение rect вправо относительно спрайта
        self.rect.x += self.rect_offset_x  # Сдвигаем rect вправо внутри спрайта
        self.facing_right = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_FORCE
        self.on_ground = False
        self.health = 100
        self.is_alive = True
        

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True

        if not self.on_ground and self.velocity_y >= 0:
            self.animator.set_state("fall" if self.facing_right else "fall_flip")
        if self.on_ground:
            state = "run" if self.velocity_x else "idle"
        else:
            state = self.animator.current_state  # Сохраняем текущее состояние в воздухе
        state += "_flip" if not self.facing_right else ""
        self.animator.set_state(state)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.on_ground:
                self.velocity_y = -self.jump_power
                self.on_ground = False
                self.animator.set_state("jump" if self.facing_right else "jump_flip")

    def update(self, platforms, camera):
        """Обновляет состояние игрока"""
        if not self.is_alive:
            return
        self.image = self.animator.update()
        old_x, old_y = self.rect.x, self.rect.y
        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, 15)
        safe_platforms = [p for p in platforms if not p.get('is_deadly', False)]
        self.rect.x, self.rect.y = handle_collisions(self, safe_platforms, camera,
                                                    self.velocity_x, self.velocity_y,
                                                    old_x, old_y)
        for platform in platforms:
            if 'is_deadly' in platform and platform['is_deadly'] and self.rect.colliderect(platform['rect']):
                self.respawn()
        if self.velocity_y < 0:
                self.animator.set_state("jump" if self.facing_right else "jump_flip")
        elif self.velocity_y > 0:
                self.animator.set_state("fall" if self.facing_right else "fall_flip")
        else:
            state = "idle" if self.velocity_x == 0 else "run"
            state += "_flip" if not self.facing_right else ""
            self.animator.set_state(state)


    def draw(self, screen, camera=None):
        """Отрисовывает игрока с учетом камеры"""
        if not self.is_alive:
            return
        pos = camera.apply(self.rect).topleft if camera else self.rect.topleft
        adjusted_pos = (pos[0] - self.rect_offset_x, pos[1])
        screen.blit(self.image, adjusted_pos)
    
    def respawn(self, x=INIT_X, y=INIT_Y):
        self.rect.topleft = (x, y)
        # Уменьшаем ширину rect и корректируем позицию
        original_width = self.image.get_width()
        new_width = int(original_width * 0.6)
        self.rect.width = new_width
        self.rect_offset_x = 14  # Смещение rect вправо
        self.rect.x += self.rect_offset_x
        self.health = 100
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.animator.set_state("idle")