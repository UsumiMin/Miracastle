import pygame
from settings import *
import json

class LevelConstruct:
    def __init__(self):
        self.platforms = []  # Будем хранить платформы для отрисовки
        self.level_data = None
        self.x_coord = 0
        self.y_coord = 0
    
    def load(self, level_name = 'level_1'):
        self.platforms = []
        self.level_data = None
        level_path = os.path.join(DATA_PATH, "levels", f"{level_name}.json")
        try:
            with open(level_path, 'r') as file:
                self.level_data = json.load(file)['structure']
        except Exception as e:
            print(f"Error loading level {level_name}: {e}")
            self.level_data = [[]]  # Пустой уровень в случае ошибки

        self.x_coord = 0
        self.y_coord = 0
        for row in self.level_data:
            for col in row:
                if col == "-":
                    platform = {
                        'surface': pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)),
                        'rect': pygame.Rect(self.x_coord, self.y_coord, PLATFORM_WIDTH, PLATFORM_HEIGHT),
                        'is_deadly': False
                    }
                    platform['surface'].fill(pygame.Color(PLATFORM_COLOR))
                    self.platforms.append(platform)
                elif col == "x":
                    platform = {
                        'surface': pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT)),  # Пустая поверхность для невидимости
                        'rect': pygame.Rect(self.x_coord, self.y_coord, PLATFORM_WIDTH, PLATFORM_HEIGHT),
                        'is_deadly': True
                    }
                    self.platforms.append(platform)
                self.x_coord += PLATFORM_WIDTH
            self.y_coord += PLATFORM_HEIGHT
            self.x_coord = 0

        self.level_width = len(self.level_data[0]) * PLATFORM_WIDTH if self.level_data and self.level_data[0] else 0
        self.level_height = len(self.level_data) * PLATFORM_HEIGHT if self.level_data else 0
        print(f"Level loaded: {len(self.platforms)} platforms, size: {self.level_width}x{self.level_height}")              #на каждой новой строчке начинаем с нуля

    def draw(self, screen, camera=None):
        for platform in self.platforms:
            if not platform['is_deadly']:  # Отрисовываем только не смертельные платформы
                if camera:
                    adjusted_rect = camera.apply(platform['rect'])
                    screen.blit(platform['surface'], adjusted_rect)
                else:
                    screen.blit(platform['surface'], platform['rect'])

    def get_level_size(self):
        return self.level_width, self.level_height