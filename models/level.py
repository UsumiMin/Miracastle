import pygame
from settings import *
import json
from utils.sprite_loader import SpriteLoader
from models.enemy import Enemy

class Level:
    def __init__(self):
        self.platforms = []
        self.enemies = []
        self.door = None
        self.level_data = None
        self.x_coord = 0
        self.y_coord = 0
        self.start_pos = (INIT_X, INIT_Y)
        self.level_elements = SpriteLoader.load_static_elements("level")
        self.backgrounds = SpriteLoader.load_static_elements("backgrounds")
        self.level_width = 0
        self.level_height = 0

    def _load_level_data(self, level_name='1'):
        level_path = os.path.join(DATA_PATH, "levels", f"level_{level_name}.json")
        with open(level_path, 'r') as file:
            self.level_data = json.load(file)['structure']


    def _create_platform(self, x, y, is_deadly=False):
        if is_deadly:
            platform_img = self.level_elements["deadly_block"][0]
            platform_surface = pygame.transform.scale(platform_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        else:
            platform_img = self.level_elements["block"][0]
            platform_surface = pygame.transform.scale(platform_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
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
        self.enemies.clear()
        self.door = None

        for row in self.level_data:
            for col in row:
                if col == "-":
                    self.platforms.append(self._create_platform(self.x_coord, self.y_coord))
                elif col == "x":
                    self.platforms.append(self._create_platform(self.x_coord, self.y_coord, is_deadly=True))
                elif col == "d" and self.door is None:
                    door_img = self.level_elements["door"][0]
                    self.door = {
                        'surface': pygame.transform.scale(door_img, (PLATFORM_WIDTH, PLATFORM_HEIGHT*2)),
                        'rect': pygame.Rect(self.x_coord, self.y_coord, PLATFORM_WIDTH, PLATFORM_HEIGHT*2)
                    }
                
                elif col == "p":
                    self.start_pos = (self.x_coord, self.y_coord)
                elif col == "f":
                    self.enemies.append(Enemy(self.x_coord, self.y_coord))
                self.x_coord += PLATFORM_WIDTH
            self.y_coord += PLATFORM_HEIGHT
            self.x_coord = 0

    def load(self, level_name='1'):
        self._load_level_data(level_name)
        self._process_level_structure()
        self._calculate_level_size()
        self.background = pygame.transform.scale(self.backgrounds["level_background"][0], (self.level_width, self.level_height))

    def _calculate_level_size(self):
        self.level_width = len(self.level_data[0]) * PLATFORM_WIDTH if self.level_data and self.level_data[0] else 0
        self.level_height = len(self.level_data) * PLATFORM_HEIGHT if self.level_data else 0

    def get_level_size(self):
        return self.level_width, self.level_height

    def get_start_pos(self):
        return self.start_pos

    def get_door(self):
        return self.door

    def get_enemies(self):
        return self.enemies