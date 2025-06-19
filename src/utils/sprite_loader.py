import os
import pygame
import json
from settings import *

class SpriteLoader:
    @staticmethod
    def _load_and_process_image(img_path, scale=1, convert_alpha=True):
        img = pygame.image.load(img_path)
        if convert_alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
        if scale != 1:
            new_size = (int(img.get_width() * scale), int(img.get_height() * scale))
            img = pygame.transform.scale(img, new_size)
        return img

    @staticmethod
    def load_animated_sprites(element_name, scale=1, convert_alpha=True):
        sprite_data = SpriteLoader._load_sprite_data(element_name)
        if not sprite_data or "states" not in sprite_data:
            raise ValueError(f"No animated sprite data found for {element_name}")
        sprite_path = os.path.join(ASSETS_PATH, *sprite_data["sprite_path"])
        sprites = {}
        for state in sprite_data["states"]:
            path = os.path.join(sprite_path, state)
            state_sprites = SpriteLoader.load_sprites(path, scale, convert_alpha)
            if state_sprites:
                sprites[state] = state_sprites
                flip_state = f"{state}_flip"
                sprites[flip_state] = [pygame.transform.flip(img, True, False) for img in sprites[state]]
        return sprites

    @staticmethod
    def load_static_elements(element_name, scale=1, convert_alpha=True):
        sprite_data = SpriteLoader._load_sprite_data(element_name)
        if not sprite_data or "elements" not in sprite_data:
            raise ValueError(f"No static elements data found for {element_name}")
        sprite_path = os.path.join(ASSETS_PATH, *sprite_data["sprite_path"])
        if not os.path.isdir(sprite_path):
            raise ValueError(f"Папка {sprite_path} не найдена")
        elements = {}
        for elem in sprite_data["elements"]:
            matching_files = [f for f in os.listdir(sprite_path) if f.startswith(elem) and f.endswith((".png", ".jpg"))]
            if matching_files:
                img_path = os.path.join(sprite_path, matching_files[0])
                elements[elem] = [SpriteLoader._load_and_process_image(img_path, scale, convert_alpha)]
        if not elements:
            raise ValueError(f"No static elements found for {element_name} in {sprite_path}")
        return elements

    @staticmethod
    def load_sprites(path, scale=1, convert_alpha=True):
        """Загружает все спрайты из папки и масштабирует их."""
        if not os.path.isdir(path):
            return []
        sprites = []
        sprites = [SpriteLoader._load_and_process_image(os.path.join(path, file), scale, convert_alpha)
                  for file in sorted(os.listdir(path))
                  if file.endswith((".png", ".jpg"))]
        return sprites

    @staticmethod
    def _load_sprite_data(element_name):
        sprites_path = os.path.join(DATA_PATH, "sprites.json")
        if not os.path.exists(sprites_path):
            raise FileNotFoundError("sprites.json not found")
        with open(sprites_path, 'r') as file:
            data = json.load(file)["sprites"]
            for key, value in data.items():
                if key == element_name:
                    return value
        return None
