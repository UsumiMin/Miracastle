import pygame
from utils.sprite_loader import SpriteLoader
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_data = SpriteLoader.load_static_elements("menu")
        self.background = self.menu_data["background"][0]  # Предполагаем один фон
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
        self.active = True

    def _handle_main_state(self, mouse_pos):
        """Обрабатывает клики в главном меню."""
        for action, button in self.buttons.items():
            if button["rect"].collidepoint(mouse_pos):
                if action == "new_game":
                    self.active = False
                    return "new_game"
                elif action == "load_game":
                    self.active = False
                    return "load_game"
                elif action == "settings":
                    self.state = "settings"
                elif action == "exit":
                    return False
        return True

    def _handle_settings_state(self, mouse_pos):
        """Обрабатывает клики в меню настроек."""
        for action, button in self.settings_buttons.items():
            if button["rect"].collidepoint(mouse_pos):
                if action == "toggle_sound":
                    self.sound_on = not self.sound_on
                    pygame.mixer.music.set_volume(1.0 if self.sound_on else 0.0)
                elif action == "toggle_fullscreen":
                    self.fullscreen = not self.fullscreen
                    pygame.display.toggle_fullscreen()
                elif action == "back":
                    self.state = "main"
        return True

    def _handle_paused_state(self, mouse_pos):
        """Обрабатывает клики в меню паузы."""
        for action, button in self.paused_buttons.items():
            if button["rect"].collidepoint(mouse_pos):
                if action == "back":
                    return "resume"
                elif action == "to_menu":
                    self.state = "main"
                    return "to_menu"
        return True

    def handle_events(self, events):
        """Обрабатывает события меню."""
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.state == "main":
                    return self._handle_main_state(mouse_pos)
                elif self.state == "settings":
                    return self._handle_settings_state(mouse_pos)
                elif self.state == "paused":
                    return self._handle_paused_state(mouse_pos)
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