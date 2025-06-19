import pygame
from utils.sprite_loader import SpriteLoader
from settings import *

class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.menu_data = SpriteLoader.load_static_elements("menu")
        self.background = self.menu_data["background"][0]
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.buttons = {
            "new_game": {"image": self.menu_data["new_game"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 0, BUTTONS_WIDTH, BUTTONS_HEIGHT)},
            "load_game": {"image": self.menu_data["load_game"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 1, BUTTONS_WIDTH, BUTTONS_HEIGHT)},
            "settings": {"image": self.menu_data["settings"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 2, BUTTONS_WIDTH, BUTTONS_HEIGHT)},
            "exit": {"image": self.menu_data["exit"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 3, BUTTONS_WIDTH, BUTTONS_HEIGHT)}
        }
        self.settings_buttons = {
            "toggle_sound": {"image": self.menu_data["toggle_sound"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 0, BUTTONS_WIDTH, BUTTONS_HEIGHT)},
            "toggle_fullscreen": {"image": self.menu_data["toggle_fullscreen"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 1, BUTTONS_WIDTH, BUTTONS_HEIGHT)},
            "back": {"image": self.menu_data["back"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 2, BUTTONS_WIDTH, BUTTONS_HEIGHT)}
        }
        self.paused_buttons = {
            "back": {"image": self.menu_data["back"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 0, BUTTONS_WIDTH, BUTTONS_HEIGHT)},
            "to_menu": {"image": self.menu_data["to_menu"][0], "rect": pygame.Rect(BUTTONS_X, BUTTONS_START + BUTTONS_STEP * 1, BUTTONS_WIDTH, BUTTONS_HEIGHT)}
        }
        self.state = "main"
        self.sound_on = True
        self.fullscreen = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        if self.state == "main":
            for button in self.buttons.values():
                self.screen.blit(button["image"], button["rect"].topleft)
        elif self.state == "settings":
            for button in self.settings_buttons.values():
                self.screen.blit(button["image"], button["rect"].topleft)
        elif self.state == "paused":
            for button in self.paused_buttons.values():
                self.screen.blit(button["image"], button["rect"].topleft)