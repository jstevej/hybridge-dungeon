import pygame

from framework.creature import Creature
from framework.projectile import ProjectileFactory
from framework.settings import *
from framework.throttle import ThrottleEvent


class PlayerBase(Creature):
    """
    Base class for the player. Inherits from Creature -> Sprite.

    Arguments:
    - image_file: The image file name, can be one tile or a row of tiles to be used as an animation.
    - animation_rates: The animation rates for the image tiles. The default is 0.1 seconds per
      frame. If a single value is given, it will be used for all frames. If a list of values is
      given, it specifies the rate for each frame separately.
    """
    def __init__(self, image_file=None, animation_rates=0.1):
        super().__init__(image_file, animation_rates)
        self.type = 'player'
        self.shoot_throttle = ThrottleEvent(0.5)
        self.shooter = None
        self.projectile_factory = None
        self.interact_throttle = ThrottleEvent(0.5)
        self.directions = { 'down': False, 'left': False, 'right': False, 'up': False }

    def set_shooter(self, shooter):
        self.shooter = shooter
        self.shoot_throttle.rate = shooter.rate
        self.projectile_factory = ProjectileFactory(shooter)
        if self.level is not None:
            self.projectile_factory.add_to_level(self.level)

    def add_to_level(self, level):
        super().add_to_level(level)
        if self.projectile_factory is not None:
            self.projectile_factory.add_to_level(level)

    def update(self, dt):
        super().update(dt)

        direction = pygame.Vector2(0, 0)

        if self.shooter is not None:
            if pygame.mouse.get_pressed()[0]:
                if self.shoot_throttle.update():
                    pos = self.rect.center
                    mouse_pos = self.level.sprites.visible.screen_to_world(pygame.mouse.get_pos())
                    shoot_direction = (mouse_pos[0] - pos[0], mouse_pos[1] - pos[1])
                    self.projectile_factory.create(self.rect.topleft, shoot_direction)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_s]:
            direction.y = 1
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_d]:
            direction.x = 1
        if keys[pygame.K_SPACE]:
            if self.interact_throttle.update():
                print("interact")

        if direction.magnitude() > 0:
            direction = direction.normalize()

        self.directions['down'] = direction.y > 0
        self.directions['left'] = direction.x < 0
        self.directions['right'] = direction.x > 0
        self.directions['up'] = direction.y < 0

        self.rect.x += self.speed * direction.x * dt
        self.handle_horizontal_collisions(direction)
        self.rect.y += self.speed * direction.y * dt
        self.handle_vertical_collisions(direction)
