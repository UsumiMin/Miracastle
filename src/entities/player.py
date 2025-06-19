import pygame
from utils.animation import AnimationManager
from utils.collisions import handle_collisions
from settings import *
from utils.audio import AudioManager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animator = AnimationManager("player", scale=2)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.width = self.rect.width * PLAYER_HIT
        self.rect_offset_x = PLAYER_OFFSET
        self.rect.x += self.rect_offset_x
        self.facing_right = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_FORCE
        self.on_ground = False
        self.health = PLAYER_HEALTH
        self.is_alive = True
        self.near_door = False
        self.step_timer = 0
        self.step_interval = PLAYER_STEP_INTER
        self.last_step_time = pygame.time.get_ticks()
        self.audio = AudioManager()

    def set_player_state(self, base_state):
        state = base_state + "_flip" if not self.facing_right else base_state
        self.animator.set_state(state)
        return state

    def _handle_movement_keys(self, keys):
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True

    def _handle_jump_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.on_ground:
                self.velocity_y = -self.jump_power
                self.on_ground = False
                self.audio.play_jump_sound()
                return True
        return False

    def _handle_door_event(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and self.near_door:
                return "change_level"
        return None       

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        self._handle_movement_keys(keys)
        self._handle_jump_event(events)
        return self._handle_door_event(events)


    def update(self, platforms, camera, door_rect):
        if not self.is_alive:
            self.set_player_state("die")
            if not getattr(self, 'death_sound_played', False):
                self.audio.play_death_sound()
                self.death_sound_played = True
            self.image = self.animator.update()
            return
        self.death_sound_played = False

        self.velocity_y += GRAVITY
        old_x, old_y = self.rect.x, self.rect.y

        safe_platforms = [p for p in platforms if not p.get('is_deadly', False)]
        self.rect.x, self.rect.y = handle_collisions(self, safe_platforms, self.velocity_x, self.velocity_y, old_y)

        for platform in platforms:
            if platform.get('is_deadly', False) and self.rect.colliderect(platform['rect']):
                self.is_alive = False
                return

        if door_rect and self.rect.colliderect(door_rect):
            self.near_door = True
        else:
            self.near_door = False

        current_time = pygame.time.get_ticks()
        if self.velocity_x != 0 and self.on_ground:
            if current_time - self.last_step_time >= self.step_interval:
                self.audio.play_step_sound()
                self.last_step_time = current_time

        if self.velocity_y < 0:
            self.set_player_state("jump")
        elif self.velocity_y > 0:
            self.set_player_state("fall")
        else:
            self.set_player_state("idle" if self.velocity_x == 0 else "run")
        self.image = self.animator.update()

    def draw(self, screen, camera=None):
        if not self.is_alive:
            return
        pos = camera.apply(self.rect).topleft if camera else self.rect.topleft
        adjusted_pos = (pos[0] - self.rect_offset_x, pos[1])
        screen.blit(self.image, adjusted_pos)
    
    def respawn(self, x=INIT_X, y=INIT_Y):
        self.rect.topleft = (x, y)
        original_width = self.image.get_width()
        new_width = int(original_width * PLAYER_HIT)
        self.rect.width = new_width
        self.rect_offset_x = PLAYER_OFFSET
        self.rect.x += self.rect_offset_x
        self.health = PLAYER_HEALTH
        self.is_alive = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.death_animation_complete = False
        self.death_sound_played = False
        self.set_player_state("idle")