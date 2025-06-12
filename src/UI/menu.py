import pygame
from utils.sprite_loader import SpriteLoader
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_data = SpriteLoader.load_character_data("menu")
        self.background = self.menu_data["sprites"]["background"][0]  # Предполагаем один фон
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.buttons = {
            "new_game": {"image": self.menu_data["sprites"]["new_game"][0], "rect": pygame.Rect(300, 200, 200, 50)},
            "load_game": {"image": self.menu_data["sprites"]["load_game"][0], "rect": pygame.Rect(300, 260, 200, 50)},
            "settings": {"image": self.menu_data["sprites"]["settings"][0], "rect": pygame.Rect(300, 320, 200, 50)},
            "exit": {"image": self.menu_data["sprites"]["exit"][0], "rect": pygame.Rect(300, 380, 200, 50)}
        }
        self.settings_buttons = {
            "toggle_sound": {"image": self.menu_data["sprites"]["toggle_sound"][0], "rect": pygame.Rect(300, 200, 200, 50)},
            "toggle_fullscreen": {"image": self.menu_data["sprites"]["toggle_fullscreen"][0], "rect": pygame.Rect(300, 260, 200, 50)},
            "back": {"image": self.menu_data["sprites"]["back"][0], "rect": pygame.Rect(300, 320, 200, 50)}
        }
        self.paused_buttons = {
            "back": {"image": self.menu_data["sprites"]["back"][0], "rect": pygame.Rect(300, 200, 200, 50)},
            "to_menu": {"image": self.menu_data["sprites"]["to_menu"][0], "rect": pygame.Rect(300, 260, 200, 50)}
        }
        self.state = "main"  # Состояния: "main" или "settings"
        self.sound_on = True
        self.fullscreen = False
        self.active = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.state == "main":
                    for action, button in self.buttons.items():
                        if button["rect"].collidepoint(mouse_pos):
                            if action == "new_game":
                                self.active = False
                                return "new_game"
                            elif action == "load_game":
                                print("Функция 'Прошлая игра' пока не реализована")
                            elif action == "settings":
                                self.state = "settings"
                            elif action == "exit":
                                return False
                elif self.state == "settings":
                    for action, button in self.settings_buttons.items():
                        if button["rect"].collidepoint(mouse_pos):
                            if action == "toggle_sound":
                                self.sound_on = not self.sound_on
                                pygame.mixer.music.set_volume(1.0 if self.sound_on else 0.0)
                            elif action == "toggle_fullscreen":
                                self.fullscreen = not self.fullscreen
                                if self.fullscreen:
                                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                                else:
                                    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                            elif action == "back":
                                self.state = "main"
                elif self.state == "paused":
                    for action, button in self.paused_buttons.items():
                        if button["rect"].collidepoint(mouse_pos):
                            if action == "back":
                                return "resume"
                            elif action == "to_menu":
                                self.state = "main"
                                return "to_menu"
        return True

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