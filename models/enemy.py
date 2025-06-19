import pygame
from utils.animation import AnimationManager
from utils.collisions import handle_collisions
from settings import *
from utils.audio import AudioManager

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.animator = AnimationManager("flower", scale=2)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(topleft=(x, y))
        original_width = self.rect.width
        original_height = self.rect.height
        self.rect.width = original_width + ENEMY_OFFSET_X  
        self.rect.height = original_height + ENEMY_OFFSET_Y
        self.rect_offset_x = -ENEMY_OFFSET_X//2
        self.rect.x += self.rect_offset_x
        self.rect.y += ENEMY_OFFSET_X
        self.rect.x -= (self.rect.width - original_width) // 2
        self.rect.y -= (self.rect.height - original_height) // 2
        self.facing_right = True
        self.speed = ENEMY_SPEED
        self.velocity_x = self.speed
        self.velocity_y = 0
        self.patrol_range = ENEMY_WALK_RANGE * PLATFORM_WIDTH
        self.start_x = x
        self.health = ENEMY_HEALTH
        self.is_alive = True
        self.is_attacking = False
        self.attack_start_time = 0
        self.audio = AudioManager()
        self.state = 'idle'


    def update(self, player):
        if not self.is_alive:
            return
        if self.rect.x <= self.start_x - self.patrol_range / 2:
            self.facing_right = True
            self.velocity_x = self.speed
            self.state = 'idle'
        elif self.rect.x >= self.start_x + self.patrol_range / 2:
            self.facing_right = False
            self.velocity_x = -self.speed
            self.state = 'idle'
        if player.is_alive:
            player_block = player.rect.x // PLATFORM_WIDTH
            enemy_block = self.rect.x // PLATFORM_WIDTH
            current_time = pygame.time.get_ticks()
            if abs(player_block - enemy_block) <= 1 and abs(player.rect.centery - self.rect.centery) < PLATFORM_HEIGHT and not self.is_attacking:
                self.is_attacking = True
                self.velocity_x = 0
                self.facing_right = player.rect.centerx > self.rect.centerx
                self.state = 'attack'
                self.attack_start_time = current_time
            if self.is_attacking and (current_time - self.attack_start_time >= ENEMY_ATTACK_MAX or abs(player_block - enemy_block) > ENEMY_ATTACK_RANGE):
                self.is_attacking = False
                self.velocity_x = self.speed if self.facing_right else -self.speed
                self.state = 'idle'
        else:
            self.is_attacking = False
            self.velocity_x = self.speed if self.facing_right else -self.speed
            self.state = 'idle'
        self.set_state(self.state)

    def update_physics(self, platforms):
        self.velocity_y += GRAVITY
        old_y = self.rect.y
        safe_platforms = [p for p in platforms if not p.get('is_deadly', False)]
        self.rect.x, self.rect.y = handle_collisions(self, safe_platforms, self.velocity_x, self.velocity_y, old_y)
        self.on_ground = any(self.rect.bottom == p['rect'].top and self.velocity_y >= 0 for p in safe_platforms)

    def set_state(self, state):
        state = state + "_flip" if not self.facing_right else state
        self.animator.set_state(state)

    def attack(self, player):
        if self.is_attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_start_time >= ENEMY_ATTACK_HIT and player.health > 0:
                self.audio.play_flower_attack()
                if player.is_alive and abs(player.rect.centery - self.rect.centery) < PLATFORM_HEIGHT:
                    player.health -= PLAYER_HEALTH
                    if player.health <= 0:
                        player.is_alive = False