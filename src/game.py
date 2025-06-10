import pygame
from settings import *
from levels.level_manager import LevelConstruct as Level
from entities.player import Player
from UI.camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Miracastle")
        self.running = True
        self.clock = pygame.time.Clock()
        self.state = Level()
        self.state.load("level_1")
        level_width, level_height = self.state.get_level_size()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
        self.player = Player(INIT_X, INIT_Y)
        self.game_state = "playing"

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Пауза на клавишу P
                    self.game_state = "paused" if self.game_state == "playing" else "playing"
        if self.game_state == "playing":
            self.player.handle_events(events)

    def update(self):
        """Обновляет состояние игры"""
        if self.game_state == "playing":
            if not self.player.is_alive:
                self.player.respawn()  # Изменено на respawn
            self.camera.update(self.player)
            self.player.update(self.state.platforms, self.camera)

    def draw(self):
        """Отрисовывает игру"""
        self.screen.fill(BLUE)
        if self.game_state == "playing":
            self.state.draw(self.screen, self.camera)
            self.player.draw(self.screen, self.camera)
            # Отладочная отрисовка платформ
            for platform in self.state.platforms:
                pygame.draw.rect(self.screen, (255, 0, 0), self.camera.apply(platform['rect']), 2)
        elif self.game_state == "paused":
            font = pygame.font.Font(None, 74)
            text = font.render("Paused", True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()  # Завершаем pygame при выходе