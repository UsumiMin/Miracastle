import pygame
import os
from settings import ASSETS_PATH

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_path = os.path.join(ASSETS_PATH, "music", "background_music.wav")
        self.button_click_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "sound", "menu_button.mp3"))
        self.door_open_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "sound", "door_open.mp3"))
        self.flower_attack_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "sound", "flower_attack.mp3"))
        self.death_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "sound", "player_death.mp3"))
        self.jump_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "sound", "player_jump.mp3"))
        self.step_sound = pygame.mixer.Sound(os.path.join(ASSETS_PATH, "sound", "player_step.mp3"))
    
    def play_background_music(self):
        """Загружает и запускает фоновую музыку на бесконечное воспроизведение."""
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)  # -1 для бесконечного повтора
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")

    def stop_music(self):
        """Останавливает воспроизведение музыки."""
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        """Устанавливает громкость музыки (0.0 - 1.0)."""
        pygame.mixer.music.set_volume(volume)

    def play_button_click(self):
        """Воспроизводит звук нажатия кнопки."""
        self.button_click_sound.play()

    def play_door_open(self):
        """Воспроизводит звук открытия двери."""
        self.door_open_sound.play()

    def play_flower_attack(self):
        """Воспроизводит звук атаки цветка."""
        self.flower_attack_sound.play()
    
    def play_death_sound(self):
        """Воспроизводит звук смерти."""
        self.death_sound.play()

    def play_jump_sound(self):
        """Воспроизводит звук прыжка."""
        self.jump_sound.play()

    def play_step_sound(self):
        """Воспроизводит звук шагов."""
        self.step_sound.play()