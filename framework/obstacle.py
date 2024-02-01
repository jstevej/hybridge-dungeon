import pygame

from framework.settings import *


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, level, image, pos=(0, 0), obstacle_above=False, obstacle_below=False):
        super().__init__(level.sprites.visible, level.sprites.obstacles)
        self.type = 'obstacle'
        self.layer_index = level.obstacle_layer_index
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.overlap_bottom = 0 if obstacle_below else 30
        self.overlap_top = 0 if obstacle_above else 20
        self.moverect = self.rect.copy()
        self.moverect.height -= self.overlap_bottom + self.overlap_top
        self.moverect.top += self.overlap_top

        for y in range(self.overlap_top):
            for x in range(self.rect.width):
                self.mask.set_at((x, y), 0)
        for y in range(self.rect.height - self.overlap_bottom, self.rect.height):
            for x in range(self.rect.width):
                self.mask.set_at((x, y), 0)
