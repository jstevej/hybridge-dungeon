import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.player_layer_index = 0
        self.offset = pygame.Vector2()

    def custom_draw(self, surface, player):
        surf_size = surface.get_size()
        self.offset.x = player.rect.centerx - int(surf_size[0] / 2)
        self.offset.y = player.rect.centery - int(surf_size[1] / 2)
        self.player_layer_index = player.layer_index

        for sprite in sorted(self.sprites(), key=self.get_sprite_sort_key):
            offset = sprite.rect.topleft - self.offset
            surface.blit(sprite.image, offset)

    def get_sprite_sort_key(self, sprite):
        is_player_layer = int(sprite.layer_index == self.player_layer_index)
        return 1e5 * sprite.layer_index + is_player_layer * sprite.rect.centery

    def screen_to_world(self, pos):
        return (pos[0] + self.offset.x, pos[1] + self.offset.y)
