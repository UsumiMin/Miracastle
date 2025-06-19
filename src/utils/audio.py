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
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(-1)

    def play_button_click(self):
        self.button_click_sound.play()

    def play_door_open(self):
        self.door_open_sound.play()

    def play_flower_attack(self):
        self.flower_attack_sound.play()
    
    def play_death_sound(self):
        self.death_sound.play()

    def play_jump_sound(self):
        self.jump_sound.play()

    def play_step_sound(self):
        self.step_sound.play()