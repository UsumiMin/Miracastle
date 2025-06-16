import pygame
from settings import *
import json
from utils.sprite_loader import SpriteLoader
from entities.enemy import Enemy

class LevelConstruct:
    def __init__(self):
        self.platforms = []  
        self.enemies = [] 
        self.door = None
        self.level_data = None
        self.x_coord = 0
        self.y_coord = 0
        self.start_pos = (INIT_X, INIT_Y)
        self.level_elements = SpriteLoader.load_static_elements("level")

    def _load_level_data(self, level_name='level_1'):
        """Загружает данные уровня из JSON-файла."""
        level_path = os.path.join(DATA_PATH, "levels", f"{level_name}.json")
        try:
            with open(level_path, 'r') as file:
                self.level_data = json.load(file)['structure']
        except Exception as e:
            print(f"Ошибка загрузки уровня {level_name}: {e}")
            self.level_data = [[]] 

    def _create_platform(self, x, y, is_deadly=False):
        """Создаёт платформу с заданными координатами и свойствами."""
        if is_deadly:  # Спрайт для смертельных платформ
            platform_img = self.level_elements["deadly_block"][0]
            platform_surface = pygame.transform.scale(platform_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        elif not is_deadly:  # Используем ассет только для обычных платформ
            platform_img = self.level_elements["block"][0]
            platform_surface = pygame.transform.scale(platform_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        else:
            platform_surface = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))  # Пустая поверхность для смертельных платформ

        platform = {
            'surface': platform_surface,
            'rect': pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT),
            'is_deadly': is_deadly
        }
        return platform
    
    def _process_level_structure(self):
        """Обрабатывает структуру уровня и создаёт платформы, дверь и начальную позицию."""
        self.x_coord = 0
        self.y_coord = 0
        self.platforms.clear()
        self.door = None
        
        self.enemies.clear()

        for row in self.level_data:
            for col in row:
                if col == "-":
                    self.platforms.append(self._create_platform(self.x_coord, self.y_coord))
                elif col == "x":
                    self.platforms.append(self._create_platform(self.x_coord, self.y_coord, is_deadly=True))
                elif col == "d" and self.door is None:
                    if "door" in self.level_elements:
                        door_img = self.level_elements["door"][0]
                        self.door = {
                            'surface': pygame.transform.scale(door_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT*2)),
                            'rect': pygame.Rect(self.x_coord, self.y_coord, PLATFORM_WIDTH, PLATFORM_HEIGHT*2)
                        }
                    else:
                        print("Ошибка: дверь не загружена")
                elif col == "p":
                    self.start_pos = (self.x_coord, self.y_coord)
                elif col == "f":  # Новый символ для врага
                    self.enemies.append(Enemy(self.x_coord, self.y_coord))
                self.x_coord += PLATFORM_WIDTH
            self.y_coord += PLATFORM_HEIGHT
            self.x_coord = 0

    def _calculate_level_size(self):
        """Вычисляет размеры уровня на основе данных."""
        self.level_width = len(self.level_data[0]) * PLATFORM_WIDTH if self.level_data and self.level_data[0] else 0
        self.level_height = len(self.level_data) * PLATFORM_HEIGHT if self.level_data else 0

    def load(self, level_name='level_1'):
        """Загружает уровень, разбивая процесс на этапы."""
        self._load_level_data(level_name)
        self._process_level_structure()
        self._calculate_level_size()             #на каждой новой строчке начинаем с нуля
        print(f"Уровень загружен: {len(self.platforms)} платформ, размер: {self.level_width}x{self.level_height}")

    def draw(self, screen, camera=None):
        for platform in self.platforms:
            if camera:
                adjusted_rect = camera.apply(platform['rect'])
                screen.blit(platform['surface'], adjusted_rect)
            else:
                screen.blit(platform['surface'], platform['rect'])
        if self.door:
            if camera:
                adjusted_rect = camera.apply(self.door['rect'])
                screen.blit(self.door['surface'], adjusted_rect)
            else:
                screen.blit(self.door['surface'], self.door['rect'])
        for enemy in self.enemies:
            enemy.draw(screen, camera)

    def get_level_size(self):
        return self.level_width, self.level_height

    def get_start_pos(self):
        return self.start_pos

    def get_door(self):
        return self.door
    def get_enemies(self):
        return self.enemies