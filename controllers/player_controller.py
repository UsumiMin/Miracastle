import pygame
from utils.audio import AudioManager

class PlayerController:
    def __init__(self, player):
        self.player = player
        self.audio = AudioManager()

    def _handle_movement_keys(self, keys):
        self.player.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.player.velocity_x = -self.player.speed
            self.player.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.player.velocity_x = self.player.speed
            self.player.facing_right = True

    def _handle_jump_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.player.on_ground:
                    self.player.velocity_y = -self.player.jump_power
                    self.player.on_ground = False
                    self.audio.play_jump_sound()
                return True
        return False

    def _handle_door_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.player.near_door:
                return "change_level"
        return None

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self._handle_movement_keys(keys)
        self._handle_jump_event(events)
        return self._handle_door_event(events)
    
    def update(self, platforms, door_rect=None):
        if not self.player.is_alive:
            self.player.set_state("die")
            if not getattr(self.player, 'death_sound_played', False):
                self.audio.play_death_sound()
                self.player.death_sound_played = True
            return

        self.player.death_sound_played = False
        self.player.update_physics(platforms)
        self.player.update_state(door_rect)

        current_time = pygame.time.get_ticks()
        if self.player.velocity_x != 0 and self.player.on_ground:
            if current_time - self.player.last_step_time >= self.player.step_interval:
                self.audio.play_step_sound()
                self.player.last_step_time = current_time
        
        if self.player.velocity_y < 0:
            state = "jump"
        elif self.player.velocity_y > 0:
            state = "fall"
        else:
            state = "idle" if self.player.velocity_x == 0 else "run"
        self.player.set_state(state)