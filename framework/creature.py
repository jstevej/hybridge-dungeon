import math
import pygame

from framework.animation import Animation
from framework.settings import *


class Creature(pygame.sprite.Sprite):
    """
    Base class for a creature.

    Arguments:
    - image_file: The image file name, can be one tile or a row of tiles to be used as an animation.
    - animation_rates: The animation rates for the image tiles. The default is 0.1 seconds per
      frame. If a single value is given, it will be used for all frames. If a list of values is
      given, it specifies the rate for each frame separately.
    """
    def __init__(self, image_file=None, animation_rates=0.1):
        super().__init__()
        self.type = 'creature'
        self.level = None
        self.layer_index = 0

        image = pygame.image.load(image_file).convert_alpha()
        image_rect = image.get_rect()
        if image_rect.height != TILE_SIZE:
            print(f"WARNING: player image height ({image_rect.height}) != {TILE_SIZE}")
        images = []
        if image_rect.width > image_rect.height:
            num_images = math.ceil(image_rect.width / image_rect.height)
            for i in range(num_images):
                x = i * image_rect.height
                images.append(image.subsurface((x, 0, image_rect.height, image_rect.height)))
        else:
            images.append(image)
        self.animation = Animation(images, animation_rates)
        self.image = images[0]

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 4.6 * TILE_SIZE

    def add_to_level(self, level):
        self.level = level
        self.kill() # remove from previous level (groups)
        if self.type == 'player':
            self.add(level.sprites.visible)
        else:
            self.add(level.sprites.visible, level.sprites.obstacles)
        self.layer_index = level.obstacle_layer_index

    def handle_horizontal_collisions(self, direction):
        for sprite in self.level.sprites.obstacles:
            rect = sprite.rect if not hasattr(sprite, 'moverect') else sprite.moverect
            if self.rect.colliderect(rect):
                if direction.x > 0:  # moving right
                    self.rect.right = rect.left
                elif direction.x < 0:  # moving left
                    self.rect.left = rect.right

    def handle_vertical_collisions(self, direction):
        for sprite in self.level.sprites.obstacles:
            rect = sprite.rect if not hasattr(sprite, 'moverect') else sprite.moverect
            overlap_top = sprite.overlap_top if hasattr(sprite, 'overlap_top') else 0
            overlap_bottom = sprite.overlap_bottom if hasattr(sprite, 'overlap_bottom') else 0
            if self.rect.colliderect(rect):
                if direction.y > 0:  # moving down
                    self.rect.bottom = sprite.rect.top + overlap_top
                elif direction.y < 0:  # moving up
                    self.rect.top = sprite.rect.bottom - overlap_bottom

    @property
    def is_idle(self):
        return not any(self.directions.values())

    def set_layer_index(self, layer_index):
        self.layer_index = layer_index

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)

    def update(self, dt):
        self.image = self.animation.update()
