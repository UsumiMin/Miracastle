import pygame
from utils.audio import AudioManager

class MenuController:
    def __init__(self, screen, game_state, menu_view, paused=False):
        self.screen = screen
        self.game_state = game_state
        self.menu_view = menu_view
        self.paused = paused
        self.audio = AudioManager()

    def _handle_main_state(self, mouse_pos):
        for action, button in self.menu_view.buttons.items():
            if button["rect"].collidepoint(mouse_pos):
                self.audio.play_button_click()
                if action == "new_game":
                    return "new_game"
                elif action == "load_game":
                    return "load_game"
                elif action == "settings":
                    self.menu_view.state = "settings"
                elif action == "exit":
                    return False
        return True

    def _handle_settings_state(self, mouse_pos):
        for action, button in self.menu_view.settings_buttons.items():
            if button["rect"].collidepoint(mouse_pos):
                self.audio.play_button_click()
                if action == "toggle_sound":
                    self.menu_view.sound_on = not self.menu_view.sound_on
                    pygame.mixer.music.set_volume(1.0 if self.menu_view.sound_on else 0.0)
                elif action == "toggle_fullscreen":
                    self.menu_view.fullscreen = not self.menu_view.fullscreen
                    pygame.display.toggle_fullscreen()
                elif action == "back":
                    self.menu_view.state = "main"
        return True

    def _handle_paused_state(self, mouse_pos):
        for action, button in self.menu_view.paused_buttons.items():
            if button["rect"].collidepoint(mouse_pos):
                self.audio.play_button_click()
                if action == "back":
                    return "resume"
                elif action == "to_menu":
                    return "to_menu"
        return True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.paused:
                    return self._handle_paused_state(mouse_pos)
                elif self.menu_view.state == "main":
                    return self._handle_main_state(mouse_pos)
                elif self.menu_view.state == "settings":
                    return self._handle_settings_state(mouse_pos)
        return True