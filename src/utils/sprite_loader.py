import os
import pygame
import json
from settings import *


class SpriteLoader:
    @staticmethod
    def load_sprites(path, scale=1, convert_alpha=True):
        """Загружает все спрайты из папки и масштабирует их."""
        sprites = []
        for file in sorted(os.listdir(path)):
            if file.endswith((".png", ".jpg")):
                img_path = os.path.join(path, file)
                img = pygame.image.load(img_path)
                if convert_alpha:
                    img = img.convert_alpha()
                else:
                    img = img.convert()
                if scale != 1:
                    new_size = (img.get_width() * scale, img.get_height() * scale)
                    img = pygame.transform.scale(img, new_size)
                
                sprites.append(img)
        return sprites
    
    @staticmethod
    def load_character_data(character_name, scale=1):
        """Загружает данные персонажа, включая спрайты, из JSON и папок."""
        with open(os.path.join(DATA_PATH, "sprites.json"), "r") as f:
            sprites_data = json.load(f)
        character_data = sprites_data["sprites"].get(character_name)
        if not character_data:
            raise ValueError(f"Персонаж '{character_name}' не найден в characters.json")
        sprites = {}
        sprite_path = character_data["sprite_path"]
        states = character_data["states"]
        
        for state, config in states.items():
            path = os.path.join(ASSETS_PATH,*sprite_path, state)
            sprites[state] = SpriteLoader.load_sprites(path, scale)
            if not sprites[state]:
                raise ValueError(f"Список спрайтов для состояния '{state}' пуст. Проверьте папку {path}")
            if config.get("flip"):
                flip_state = f"{state}_flip"
                sprites[flip_state] = [pygame.transform.flip(img, True, False) for img in sprites[state]]
        return {"sprites": sprites, "states": states}