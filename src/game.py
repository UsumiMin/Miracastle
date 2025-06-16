import pygame
from settings import *
from levels.level_manager import LevelConstruct as Level
from entities.player import Player
from entities.enemy import Enemy
from UI.camera import Camera
from UI.menu import Menu
from utils.sprite_loader import SpriteLoader

class Game:
    def __init__(self):
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Miracastle")
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_state = "menu" 
        self.menu = Menu(self.screen)
        self.game_data = SpriteLoader.load_static_elements("backgrounds")
        self.game_background = self.game_data["level_background"][0]
        self.game_background = pygame.transform.scale(self.game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_level = "1" 
        self.state = None
        self.camera = None
        self.player = None
        self.font = pygame.font.Font(ASSETS_PATH + "/RuneScape-ENA.ttf", 36)

    def _handle_menu_events(self, events):
        """Обрабатывает события в меню."""
        result = self.menu.handle_events(events)
        if result == "new_game":
            self.game_state = "playing"
            self._initialize_game()
        elif result is False:
            self.running = False
        elif result == "to_menu":
            self.game_state = "menu"
            self._cleanup_game_objects()
        return True

    def _handle_playing_events(self, events):
        """Обрабатывает события в игре."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_state = "paused"
                self.menu.state = "paused"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and not self.player.is_alive:
                self.player.respawn(*self.state.get_start_pos())  # Перезапуск игрока
                self.game_state = "playing"  # Возвращаем в игру
        action = self.player.handle_events(events)
        if action == "change_level":
            self._change_level()
        return True

    def _handle_paused_events(self, events):
        """Обрабатывает события в паузе."""
        result = self.menu.handle_events(events)
        if result == "resume":
            self.game_state = "playing"
            self.menu.state = "main"
        elif result == "to_menu":
            self.game_state = "menu"
            self._cleanup_game_objects()
        return True

    def handle_events(self):
        """Обрабатывает все события в зависимости от состояния."""
        events = pygame.event.get()
        if self.game_state == "menu":
            return self._handle_menu_events(events)
        elif self.game_state == "playing":
            return self._handle_playing_events(events)
        elif self.game_state == "paused":
            return self._handle_paused_events(events)
        return True

    def _initialize_game(self):
        """Инициализирует игру с новым уровнем."""
        self.state = Level()
        self.state.load(f"level_{self.current_level}")
        level_width, level_height = self.state.get_level_size()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
        self.player = Player(*self.state.get_start_pos())

    def _change_level(self):
        """Меняет текущий уровень на следующий."""
        current_num = int(self.current_level)
        next_num = current_num + 1
        max_level = MAX_LEVEL
        self.current_level = str(next_num) if next_num <= max_level else "1"
        self.state.load(f"level_{self.current_level}")
        level_width, level_height = self.state.get_level_size()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
        start_pos = self.state.get_start_pos()
        self.player = Player(start_pos[0], start_pos[1])

    def _cleanup_game_objects(self):
        """Очищает объекты игры при возврате в меню."""
        if hasattr(self, 'state'):
            del self.state
        if hasattr(self, 'camera'):
            del self.camera
        if hasattr(self, 'player'):
            del self.player
        self.state = None
        self.camera = None
        self.player = None

    def update(self):
        """Обновляет состояние игры"""
        if self.game_state == "playing":
            self.camera.update(self.player)
            self.player.update(self.state.platforms, self.camera, self.state.get_door()['rect'] if self.state.get_door() else None)
            for enemy in self.state.get_enemies():
                enemy.update(self.player, self.state.platforms, self.camera)

    def draw(self):
        """Отрисовывает игру"""
        self.menu.draw()
        if self.game_state == "playing":
            self.screen.blit(self.game_background, (0, 0))
            self.state.draw(self.screen, self.camera)
            door = self.state.get_door()
            if door and self.camera:
                adjusted_rect = self.camera.apply(door['rect'])
                self.screen.blit(door['surface'], adjusted_rect)
            self.player.draw(self.screen, self.camera)
            for enemy in self.state.get_enemies():
                enemy.draw(self.screen, self.camera)
            for platform in self.state.platforms:
                pygame.draw.rect(self.screen, PLATFORM_COLOR2, self.camera.apply(platform['rect']), 2)
            # Отображение текста при смерти
            if not self.player.is_alive:
                death_text = self.font.render("Вы погибли, нажмите R", True, YELLOW)
                text_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                self.screen.blit(death_text, text_rect)
        pygame.display.update()


    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        