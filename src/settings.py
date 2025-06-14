import os
# Настройки игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CHAR_HIT = 0.45

# Получаем абсолютный путь к папке src/
BASE_DIR = os.path.abspath(os.curdir)  # Путь к src/
# Поднимаемся на уровень выше (в my_game/) и заходим в assets/
ASSETS_PATH = os.path.join(BASE_DIR, "assets")
DATA_PATH = os.path.join(BASE_DIR, "data")
# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

INIT_X = 100
INIT_Y = 100
# Физика
GRAVITY = 0.5
JUMP_FORCE = 12
PLAYER_SPEED = 5

# Платформы
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#531067"
PLATFORM_COLOR2 = "#211441"