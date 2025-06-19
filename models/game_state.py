import json
import os
from settings import *
from models.player import Player
from models.level import Level
from views.camera import Camera

class GameState:
    def __init__(self):
        self.running = True
        self.state = "menu"
        self.current_level = "1"
        self.death_count = 0
        self.background = None
        self.level = None
        self.player = None
        self.camera = None

    def initialize(self):
        self.level = Level()
        self.level.load(self.current_level)
        level_width, level_height = self.level.get_level_size()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
        self.player = Player(*self.level.get_start_pos())
        self.background = self.level.background

    def load(self):
        save_path = os.path.join(DATA_PATH, "save.json")
        try:
            with open(save_path, 'r') as file:
                save_data = json.load(file)
                self.current_level = save_data.get("current_level", "1")
                self.death_count = save_data.get("death_count", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_level = "1"
            self.death_count = 0
        self.initialize()

    def save(self):
        save_data = {
            "current_level": self.current_level,
            "death_count": self.death_count
        }
        save_path = os.path.join(DATA_PATH, "save.json")
        with open(save_path, 'w') as file:
            json.dump(save_data, file)

    def reset(self):
        self.current_level = "1"
        self.death_count = 0
        self.level = None
        self.player = None
        self.camera = None

    def cleanup(self):
        self.level = None
        self.player = None
        self.camera = None