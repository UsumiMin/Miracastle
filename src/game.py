import pygame
from settings import *
from levels.level_manager import LevelConstruct as Level
from entities.player import Player
from UI.camera import Camera
from UI.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Miracastle")
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_state = "menu" 
        self.menu = Menu(self.screen)

    def handle_events(self):
        events = pygame.event.get()
        if self.game_state == "menu":
            result = self.menu.handle_events(events)
            if result == "new_game":
                self.game_state = "playing"
                self.state = Level()
                self.state.load("level_1")
                level_width, level_height = self.state.get_level_size()
                self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
                self.player = Player(INIT_X, INIT_Y)
            elif result is False:
                self.running = False
            elif result == "to_menu":
                self.game_state = "menu"
                if hasattr(self, 'state'):
                    del self.state
                if hasattr(self, 'camera'):
                    del self.camera
                if hasattr(self, 'player'):
                    del self.player
        elif self.game_state == "playing":
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "paused"
                        self.menu.state = "paused"
            self.player.handle_events(events)
        elif self.game_state == "paused":
            result = self.menu.handle_events(events)
            if result == "resume":
                self.game_state = "playing"
                self.menu.state = "main"
            elif result == "to_menu":
                self.game_state = "menu"
                if hasattr(self, 'state'):
                    del self.state
                if hasattr(self, 'camera'):
                    del self.camera
                if hasattr(self, 'player'):
                    del self.player

    def update(self):
        """Обновляет состояние игры"""
        if self.game_state == "playing":
            if not self.player.is_alive:
                self.player.respawn()  # Изменено на respawn
            self.camera.update(self.player)
            self.player.update(self.state.platforms, self.camera)

    def draw(self):
        """Отрисовывает игру"""
        self.menu.draw()
        if self.game_state == "playing":
            self.screen.fill(BLUE)
            self.state.draw(self.screen, self.camera)
            self.player.draw(self.screen, self.camera)
            for platform in self.state.platforms:
                pygame.draw.rect(self.screen, (255, 0, 0), self.camera.apply(platform['rect']), 2)
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()  # Завершаем pygame при выходе