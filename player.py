import pygame

from framework.debug import debug
from framework.player_base import PlayerBase
from framework.settings import *
from framework.throttle import ThrottleEvent


# class LightningBall:
#     def __init__(self):
#         self.name = 'LightningBall'
#         self.rate = 0.5
#         self.image = pygame.image.load('./assets/LightningBall64.png')
#         self.speed = 10 * TILE_SIZE
#         self.damage = 2
#         self.max_distance = 10 * TILE_SIZE
#         self.bounce = False


# class ForceBall:
#     def __init__(self):
#         self.name = 'ForceBall'
#         self.rate = 0.25
#         self.image = pygame.image.load('./assets/ForceBall64.png')
#         self.speed = 14 * TILE_SIZE
#         self.damage = 1
#         self.max_distance = 14 * TILE_SIZE
#         self.bounce = True


# class FireBall:
#     def __init__(self):
#         self.name = 'FireBall'
#         self.rate = 0.75
#         self.image = pygame.image.load('./assets/FireBall64.png')
#         self.speed = 8 * TILE_SIZE
#         self.damage = 4
#         self.max_distance = 8 * TILE_SIZE
#         self.bounce = False


class Player(PlayerBase):
    def __init__(self):
        super().__init__(image_file='./assets/MasterIllusionistSprites64.png')
        # self.change_shooter_throttle = ThrottleEvent(0.1)
        # self.set_shooter(LightningBall())

    def update(self, dt):
        super().update(dt)
        info = [f"x: {self.rect.x}, y: {self.rect.y}"]
        info.append(f"visible: {len(self.level.sprites.visible)}")
        info.append(f"obstacles: {len(self.level.sprites.obstacles)}")
        info.append(f"projectiles: {len(self.level.sprites.projectiles)}")
        # shooter_name = self.shooter.name if self.shooter else 'None'
        # info.append(f"shooter: {shooter_name}")
        debug(info)

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_r]:
        #     if self.change_shooter_throttle.update():
        #         if self.shooter is None:
        #             self.set_shooter(LightningBall())
        #         elif self.shooter.name == 'LightningBall':
        #             self.set_shooter(FireBall())
        #         elif self.shooter.name == 'FireBall':
        #             self.set_shooter(ForceBall())
        #         elif self.shooter.name == 'ForceBall':
        #             self.set_shooter(LightningBall())

