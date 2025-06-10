import pygame
from utils.sprite_loader import SpriteLoader
from settings import ASSETS_PATH
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = {
            "idle": SpriteLoader.load_sprites(
                os.path.join(ASSETS_PATH, "sprites", "characters", "player", "idle"),
                scale=2
            ),
            "run": SpriteLoader.load_sprites(
                os.path.join(ASSETS_PATH, "sprites", "characters", "player", "run"),
                scale=2
            ),
            "jump": SpriteLoader.load_sprites(
                os.path.join(ASSETS_PATH, "sprites", "characters", "player", "jump"),
                scale=2
            ),
        }
        self.current_state = "idle"
        self.current_frame = 0
        self.animation_speed = 0.15
        self.image = self.sprites[self.current_state][self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        # Логика анимации
        self.current_frame += self.animation_speed * dt
        if self.current_frame >= len(self.sprites[self.current_state]):
            self.current_frame = 0
        
        self.image = self.sprites[self.current_state][int(self.current_frame)]