import pygame
from utils.animation import AnimationManager
from utils.collisions import handle_collisions
from settings import *
from utils.audio import AudioManager

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animator = AnimationManager("flower", scale=2)
        self.image = self.animator.update()
        self.rect = self.image.get_rect(topleft=(x, y))
        original_width = self.rect.width
        original_height = self.rect.height
        padding_x = -35  
        padding_y = -16  
        self.rect.width = original_width * 2 + padding_x * 2  
        self.rect.height = original_height * 2 + padding_y * 2 
        
        self.rect_offset_x = 35
        self.rect.x += self.rect_offset_x
        self.rect.x -= (self.rect.width - original_width) // 2
        self.rect.y -= (self.rect.height - original_height) // 2
        
        self.facing_right = True
        self.speed = ENEMY_SPEED
        self.velocity_x = self.speed
        self.velocity_y = 0
        self.patrol_range = 3 * PLATFORM_WIDTH
        self.start_x = x
        self.health = 50
        self.is_alive = True
        self.is_attacking = False
        self.attack_start_time = 0
        
        self.audio = AudioManager()  # Инициализация менеджера аудио


    def set_enemy_state(self, base_state):
        state = base_state + "_flip" if not self.facing_right else base_state
        self.animator.set_state(state)
        return state

    def update(self, player, platforms, camera):
        if not self.is_alive:
            return
        
        if self.rect.x <= self.start_x - self.patrol_range / 2:
            self.facing_right = True
            self.velocity_x = self.speed
        elif self.rect.x >= self.start_x + self.patrol_range / 2:
            self.facing_right = False
            self.velocity_x = -self.speed
        if player.is_alive:
            player_block = player.rect.x // PLATFORM_WIDTH
            enemy_block = self.rect.x // PLATFORM_WIDTH
            current_time = pygame.time.get_ticks()
            if abs(player_block - enemy_block) <= 1 and abs(player.rect.centery - self.rect.centery) < PLATFORM_HEIGHT and not self.is_attacking:
                self.is_attacking = True
                self.velocity_x = 0
                self.facing_right = player.rect.centerx > self.rect.centerx
                self.attack_start_time = current_time
            if self.is_attacking and (current_time - self.attack_start_time >= 1000 or abs(player_block - enemy_block) > 1):
                self.is_attacking = False
                self.velocity_x = self.speed if self.facing_right else -self.speed
        else:
            self.is_attacking = False
            self.velocity_x = self.speed if self.facing_right else -self.speed
        old_x, old_y = self.rect.x, self.rect.y
        self.velocity_y += GRAVITY
        self.velocity_y = min(self.velocity_y, 15)
        safe_platforms = [p for p in platforms if not p.get('is_deadly', False)]
        self.rect.x, self.rect.y = handle_collisions(self, safe_platforms, camera, self.velocity_x, self.velocity_y, old_x, old_y)
        if self.is_attacking:
            self.set_enemy_state("attack")
        else:
            self.set_enemy_state("run")

        self.image = self.animator.update()
        self._attack(player)

    def _attack(self, player):
        """Атака игрока, уменьшает здоровье через 2 секунды после начала атаки."""
        if self.is_attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_start_time >= 700 and player.health > 0:
                self.audio.play_flower_attack()
                if player.is_alive and abs(player.rect.centery - self.rect.centery) < PLATFORM_HEIGHT:
                    
                    player.health -= 1
                    print(f"Damage dealt at time: {current_time}")
                    if player.health <= 0:
                        player.is_alive = False

    def draw(self, screen, camera=None):
        if not self.is_alive:
            return
        pos = camera.apply(self.rect).topleft if camera else self.rect.topleft
        adjusted_pos = (pos[0] - self.rect_offset_x, pos[1])
        screen.blit(self.image, adjusted_pos)