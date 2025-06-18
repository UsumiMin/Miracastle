import pygame
import json
from settings import *
from levels.level_manager import LevelConstruct as Level
from entities.player import Player
from UI.camera import Camera
from UI.menu import Menu
from utils.sprite_loader import SpriteLoader
from utils.audio import AudioManager

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
        self.death_count = 0
        self.audio = AudioManager()  # Инициализация менеджера аудио
        self.audio.play_background_music()  # Запуск фоновой музыки

    def _handle_menu_events(self, events):
        """Обрабатывает события в меню."""
        result = self.menu.handle_events(events)
        if result == "new_game":
            self.current_level = "1"
            self.death_count = 0
            self.game_state = "intro"  # Показываем начальное окно
        elif result == "load_game":
            self._load_game()
            self.game_state = "playing"
            self._initialize_game()
        elif result is False:
            self.running = False
            self.audio.stop_music()  # Остановка музыки при выходе
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
                self.death_count += 1  # Увеличиваем счётчик смертей
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
    
    def _handle_intro_events(self, events):
        """Обрабатывает события начального окна."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                self.game_state = "playing"
                self._initialize_game()
        return True

    def _handle_game_over_events(self, events):
        """Обрабатывает события финального окна."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
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
        elif self.game_state == "intro":
            return self._handle_intro_events(events)
        elif self.game_state == "game_over":
            return self._handle_game_over_events(events)
        return True

    def _initialize_game(self):
        """Инициализирует игру с новым уровнем."""
        self.state = Level()
        self.state.load(f"level_{self.current_level}")
        self._save_game()
        level_width, level_height = self.state.get_level_size()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
        self.player = Player(*self.state.get_start_pos())

    def _change_level(self):
        """Меняет текущий уровень на следующий."""
        current_num = int(self.current_level)
        next_num = current_num + 1
        max_level = MAX_LEVEL
        self.current_level = str(next_num) if next_num <= max_level else "1"
        self.audio.play_door_open()  # Звук открытия двери при переходе
        self._save_game()
        self.state.load(f"level_{self.current_level}")
        level_width, level_height = self.state.get_level_size()
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width, level_height)
        start_pos = self.state.get_start_pos()
        self.player = Player(start_pos[0], start_pos[1])
        if next_num > max_level:  # Если прошли последний уровень
            self.game_state = "game_over"

    def _load_game(self):
        """Загружает сохранённый уровень из файла."""
        save_path = os.path.join(DATA_PATH, "save.json")
        try:
            with open(save_path, 'r') as file:
                save_data = json.load(file)
                self.current_level = save_data.get("current_level", "1")
                self.death_count = save_data.get("death_count", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_level = "1"
            self.death_count = 0

    def _save_game(self):
        """Сохраняет текущий уровень в файл."""
        save_data = {
            "current_level": self.current_level,
            "death_count": self.death_count
        }
        save_path = os.path.join(DATA_PATH, "save.json")
        with open(save_path, 'w') as file:
            json.dump(save_data, file)
            
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
            if not self.player.is_alive:
                death_text = self.font.render("Вы погибли, нажмите R", True, YELLOW)
                text_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                self.screen.blit(death_text, text_rect)
        elif self.game_state == "intro":
            self.screen.fill(BACKGROUND_COLOR)  # Серый фон
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
                text_surface = self.font.render(line, True, YELLOW)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 50
        elif self.game_state == "game_over":
            self.screen.fill(BACKGROUND_COLOR)  # Тёмный фон
            death_line = ["Хотя, сбежал ты номинально,", f"ведь ты уже успел погибнуть целых {self.death_count} раза!"] if self.death_count != 0 else ["Да, ты действительно сбежал", "ни разу не умерев. Это круто!"]
            game_over_text = [
                "Поздравляем! Ты сбежал из замка!",
                *death_line,
                "Теперь заканчивай играть и займись своими делами",
                "А, и больше не ешь ничего, что отправит тебя сюда.",
                "Прощай!"
            ]
            y_offset = SCREEN_HEIGHT // 4
            for line in game_over_text:
                text_surface = self.font.render(line, True, YELLOW)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 50
        pygame.display.update()


    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        