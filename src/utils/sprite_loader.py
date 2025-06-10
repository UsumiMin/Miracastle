import os
import pygame

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