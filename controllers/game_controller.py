import pygame
from models.game_state import GameState
from views.render import render_game, render_intro, render_game_over
from utils.audio import AudioManager
from controllers.menu_controller import MenuController
from controllers.player_controller import PlayerController
from models.player import Player
from views.menu_view import MenuView
from views.camera import Camera
from settings import *

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.audio = AudioManager()
        self.audio.play_background_music()
        self.menu_view = MenuView(screen)
        self.player_ctrl = None

    def handle_events(self, events):
        if self.game_state.state == "menu":
            return self._handle_menu_events(events)
        elif self.game_state.state == "playing":
            return self._handle_playing_events(events)
        elif self.game_state.state == "paused":
            return self._handle_paused_events(events)
        elif self.game_state.state == "intro":
            return self._handle_intro_events(events)
        elif self.game_state.state == "game_over":
            return self._handle_game_over_events(events)

    def _handle_menu_events(self, events):
        menu_ctrl = MenuController(self.screen, self.game_state, self.menu_view)
        result = menu_ctrl.handle_events(events)
        if result == "new_game":
            self.game_state.reset()
            self.game_state.state = "intro"
        elif result == "load_game":
            self.game_state.load()
            self.game_state.state = "playing"
            self.player_ctrl = PlayerController(self.game_state.player)
        elif result is False:
            self.game_state.running = False
            self.audio.stop_music()
        elif result == "to_menu":
            self.game_state.state = "menu"
            self.game_state.cleanup()
        return True

    def _handle_playing_events(self, events):
        player_ctrl = PlayerController(self.game_state.player)
        action = player_ctrl.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.game_state.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game_state.state = "paused"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and not self.game_state.player.is_alive:
                self.game_state.player.respawn(*self.game_state.level.get_start_pos())
                self.game_state.death_count += 1
                self.game_state.state = "playing"
        
        if action == "change_level":
            self._change_level()
        return True

    def _handle_paused_events(self, events):
        menu_ctrl = MenuController(self.screen, self.game_state, self.menu_view, paused=True)
        result = menu_ctrl.handle_events(events)
        if result == "resume":
            self.game_state.state = "playing"
        elif result == "to_menu":
            self.game_state.state = "menu"
            self.game_state.cleanup()
        return True

    def _handle_intro_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_state.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.game_state.initialize()
                self.game_state.state = "playing"
                self.player_ctrl = PlayerController(self.game_state.player)
        return True

    def _handle_game_over_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_state.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.game_state.state = "menu"
                self.game_state.cleanup()
        return True

    def _change_level(self):
        current_num = int(self.game_state.current_level)
        next_num = current_num + 1
        max_level = MAX_LEVEL
        self.game_state.current_level = str(next_num) if next_num <= max_level else "1"
        self.audio.play_door_open()
        self.game_state.level.load(self.game_state.current_level)
        start_pos = self.game_state.level.get_start_pos()
        self.game_state.player = Player(start_pos[0], start_pos[1])
        self.player_ctrl = PlayerController(self.game_state.player)
        level_width, level_height = self.game_state.level.get_level_size()
        self.game_state.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
        if next_num > max_level:
            self.game_state.state = "game_over"

    def update(self):
        if self.game_state.state == "playing":
            self.game_state.camera.update(self.game_state.player)
            self.player_ctrl.update(self.game_state.level.platforms, self.game_state.level.get_door()['rect'] if self.game_state.level.get_door() else None)
            for enemy in self.game_state.level.get_enemies():
                enemy.update(self.game_state.player)
                enemy.update_physics(self.game_state.level.platforms)
                enemy.attack(self.game_state.player)

    def render(self):
        if self.game_state.state == "menu":
            self.menu_view.draw()
        if self.game_state.state == "playing":
            render_game(self.screen, self.game_state.background, self.game_state.level, self.game_state.camera, self.game_state.player, self.game_state.level.get_enemies())
        elif self.game_state.state == "intro":
            render_intro(self.screen)
        elif self.game_state.state == "game_over":
            render_game_over(self.screen, self.game_state.death_count)

    def run(self):
        while self.game_state.running:
            self.clock.tick(FPS)
            events = pygame.event.get()
            self.handle_events(events)
            self.update()
            self.render()
            pygame.display.flip()