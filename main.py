from controllers.game_controller import GameController
import pygame
from settings import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Miracastle")
    game = GameController(screen)
    game.run()
    pygame.quit()