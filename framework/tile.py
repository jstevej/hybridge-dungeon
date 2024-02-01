import pygame

from framework.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, layer_index, pos, image, *args):
        super().__init__(*args)
        self.type = 'tile'
        self.layer_index = layer_index
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
