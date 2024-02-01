import pygame
from pytmx.util_pygame import load_pygame

from framework.camera_group import CameraGroup
from framework.debug import debug_draw
from framework.obstacle import Obstacle
from framework.settings import *
from framework.tile import Tile


class LevelSprites:
    def __init__(self):
        self.obstacles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.visible = CameraGroup()


class LevelBase:
    """
    Base class for levels.

    Arguments:
    - screen: the surface to draw on
    - player: the player object
    - map_file: the Tiled map file name
    - spawns: a dictionary of spawn object names to image file names or Creature classes, e.g.,
      {
          'steve': './assets/WiseWizard64.png',
          'goblin': './assets/Goblin64.png',
      }
      The spawn object names are the names of points in the Tiled "SpawnLocations" object layer. The
      values of the dictionary can either be image file names or Creature classes.
    """
    def __init__(self, screen=None, player=None, map_file=None, spawns=None):
        self.screen = screen
        self.sprites = LevelSprites()
        self.obstacle_layer_index = 2  # assume obstacles are on layer 2
        self.player = player
        self.spawns = spawns if spawns is not None else {}
        self.player.add_to_level(self)
        self.load_map(map_file)

    def add_obstacle_tile(self, tm, layer, x, y, image):
        obstacle_above = y > 0 and layer.data[y - 1][x] > 0
        obstacle_below = y < tm.height - 1 and layer.data[y + 1][x] > 0
        Obstacle(
            self,
            image,
            pos=(x * tm.tilewidth, y * tm.tileheight),
            obstacle_above=obstacle_above,
            obstacle_below=obstacle_below
        )

    def create_layer_image(self, tm, layer_name):
        layer = tm.get_layer_by_name(layer_name)
        image = pygame.Surface((tm.width * tm.tilewidth, tm.height * tm.tileheight))
        for x, y, tile_image in layer.tiles():
            image.blit(tile_image, (x * tm.tilewidth, y * tm.tileheight))
        return image

    def load_map(self, map_file_name):
        tm = load_pygame(map_file_name)

        print("layers:")
        obstacle_layer_index = None
        for i, layer in enumerate(tm.layers):
            print(f"    {i}: name: {layer.name}, visible: {layer.visible}")
            if layer.visible:
                if layer.name == 'Floor':
                    floor_image = self.create_layer_image(tm, 'Floor')
                    self.floor = Tile(i, (0, 0), floor_image, self.sprites.visible)
                else:
                    if layer.name == 'Obstacles':
                        for x, y, tile_image in layer.tiles():
                            self.add_obstacle_tile(tm, layer, x, y, tile_image)
                        obstacle_layer_index = i
                    elif layer.name == 'SpawnLocations':
                        for obj in layer:
                            if obj.name == 'player':
                                self.player.set_pos(obj.x, obj.y)
                            else:
                                spawn = self.spawns.get(obj.name)
                                if spawn is not None:
                                    if isinstance(spawn, str):
                                        spawn_image = pygame.image.load(spawn).convert_alpha()
                                        Obstacle(self, spawn_image, pos=(obj.x, obj.y))
                                    else:
                                        spawn.add_to_level(self)
                                        spawn.set_pos(obj.x, obj.y)
                                else:
                                    print(f"ERROR: spawn file not found for {obj.name}")

                    else:
                        for x, y, tile_image in layer.tiles():
                            pos = (x * tm.tilewidth, y * tm.tileheight)
                            Tile(i, pos, tile_image, self.sprites.visible)

        if obstacle_layer_index is None:
            raise AssertionError("Obstacles layer not found")

        if obstacle_layer_index != 2:
            raise AssertionError("Obstacles layer is not layer 2")


    def run(self, dt):
        self.sprites.visible.update(dt)
        self.screen.fill('black')
        self.sprites.visible.custom_draw(self.screen, self.player)
        debug_draw()
