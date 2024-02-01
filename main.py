import pygame

from framework.settings import *
from level_1 import Level1
from player import Player


class Game:
    def __init__(self):
        pygame.init()

    def run(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('HybridgeDungeon')
        clock = pygame.time.Clock()
        player = Player()
        level = Level1(screen, player)
        running = True
        dt = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            level.run(dt)

            pygame.display.flip()
            dt = clock.tick(FPS) / 1000

        pygame.quit()


game = Game()
game.run()
