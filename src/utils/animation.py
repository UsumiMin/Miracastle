import pygame
import os
from utils.sprite_loader import SpriteLoader

class AnimationManager:
    def __init__(self, sprite_path, states, scale=1, default_speed=0.10):
        self.sprites = {}
        self.current_state = "idle"
        self.current_frame = 0
        self.animation_speed = default_speed
        for state, config in states.items():
            path = os.path.join(sprite_path, state)
            sprites = SpriteLoader.load_sprites(path, scale)
            if not sprites:
                raise ValueError(f"Список спрайтов для состояния '{state}' пуст")
            self.sprites[state] = sprites
            if config.get("flip"):
                flip_state = f"{state}_flip"
                self.sprites[flip_state] = [pygame.transform.flip(img, True, False) for img in sprites]
                
    def update(self):
        self.current_frame = (self.current_frame + self.animation_speed) % len(self.sprites[self.current_state])
        return self.sprites[self.current_state][int(self.current_frame)]

    def set_state(self, state):
        if state in self.sprites and state != self.current_state:
            self.current_state = state
            self.current_frame = 0