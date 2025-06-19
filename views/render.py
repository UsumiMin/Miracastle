import pygame
from settings import *

def draw_platforms(screen, platforms, camera):
    for platform in platforms:
        adjusted_rect = camera.apply(platform['rect'])
        screen.blit(platform['surface'], adjusted_rect)

def draw_player(screen, player, camera):
    current_image = player.animator.update()
    adjusted_rect = camera.apply(player.rect)
    adjusted_pos = (adjusted_rect.left - player.rect_offset_x, adjusted_rect.top)
    screen.blit(current_image, adjusted_pos)

def draw_enemy(screen, enemy, camera):
    current_image = enemy.animator.update()
    adjusted_rect = camera.apply(enemy.rect)
    pos = camera.apply(enemy.rect).topleft if camera else enemy.rect.topleft
    adjusted_pos = (pos[0] - enemy.rect_offset_x, pos[1])
    screen.blit(current_image, adjusted_pos)
    
def render_game(screen, background, level, camera, player, enemies):
    screen.blit(background, (0, 0))
    draw_platforms(screen, level.platforms, camera)
    if level.door:
        adjusted_rect = camera.apply(level.door['rect'])
        screen.blit(level.door['surface'], adjusted_rect)
    draw_player(screen, player, camera)
    for enemy in enemies:
        draw_enemy(screen, enemy, camera)
    if not player.is_alive:
        font = pygame.font.Font(ASSETS_PATH + "/RuneScape-ENA.ttf", FONT_SIZE)
        death_text = font.render("Вы погибли, нажмите R", True, YELLOW)
        text_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - STRING_SPACE))
        screen.blit(death_text, text_rect)
        

def render_intro(screen):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(ASSETS_PATH + "/RuneScape-ENA.ttf", FONT_SIZE)
    intro_text = [
        "Ты проснулся в странном огромном садике",
        "в каком-то подозрительном замке.",
        "Ничего не понимая",
        "ты решаешь покинуть это место, но на твоём пути",
        "возникли цветы, которым ты кажешься очень вкусным.",
        "Сбеги из замка, попытавшись не умереть. Удачи!"
    ]
    y_offset = SCREEN_HEIGHT // 4
    for line in intro_text:
        text_surface = font.render(line, True, YELLOW)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 50

def render_game_over(screen, death_count):
    screen.fill(BACKGROUND_COLOR)
    death_line = ["Хотя, сбежал ты номинально,", f"ведь ты уже успел погибнуть целых {death_count} раза!"] if death_count != 0 else ["Да, ты действительно сбежал", "ни разу не умерев. Это круто!"]
    game_over_text = [
        "Поздравляем! Ты сбежал из замка!",
        *death_line,
        "Теперь заканчивай играть и займись своими делами",
        "А, и больше не ешь ничего, что отправит тебя сюда.",
        "Прощай!"
    ]
    y_offset = SCREEN_HEIGHT // 4
    font = pygame.font.Font(ASSETS_PATH + "/RuneScape-ENA.ttf", FONT_SIZE)
    for line in game_over_text:
        text_surface = font.render(line, True, YELLOW)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += STRING_SPACE