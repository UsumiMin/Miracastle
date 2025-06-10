# Настройки игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
import os
# Получаем абсолютный путь к папке src/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Путь к src/
# Поднимаемся на уровень выше (в my_game/) и заходим в assets/
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Физика
GRAVITY = 0.5
JUMP_FORCE = -12
PLAYER_SPEED = 5