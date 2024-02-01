import pygame


class Projectile(pygame.sprite.Sprite):
    """
    Class for projectiles.
    """

    def __init__(
        self,
        level,
        image,
        pos=(0, 0),
        velocity=pygame.Vector2(0, 0),
        damage=1,
        max_distance=1,
        bounce=False):
        super().__init__(level.sprites.visible, level.sprites.projectiles)
        self.type = 'projectile'
        self.level = level
        self.layer_index = level.obstacle_layer_index
        self.image = image
        self.pos = pygame.Vector2(pos)
        self.start_pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = velocity
        self.damage = damage
        self.max_distance = max_distance
        self.distance_travelled = pygame.Vector2(0, 0)
        self.bounce = bounce

    def update(self, dt):
        orig_pos = self.pos.copy()
        self.pos += self.velocity * dt
        self.distance_travelled.x += abs(self.velocity.x * dt)
        self.distance_travelled.y += abs(self.velocity.y * dt)

        if self.distance_travelled.magnitude() > self.max_distance:
            self.kill()
            return

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        for sprite in self.level.sprites.obstacles:
            if sprite.type != 'projectile' and pygame.sprite.collide_mask(self, sprite):
                #sprite.apply_damage(self.damage)
                if self.bounce:
                    p1 = pygame.Vector2(
                        orig_pos.x + 0.5 * self.rect.width,
                        orig_pos.y + 0.5 * self.rect.height)
                    p2 = pygame.Vector2(
                        self.pos.x + 0.5 * self.rect.width,
                        self.pos.y + 0.5 * self.rect.height)

                    if abs(p2.x - p1.x) < 0.0000001:
                        self.velocity.y = -self.velocity.y
                    else:
                        rect = sprite.rect if not hasattr(sprite, 'moverect') else sprite.moverect
                        m = (p2.y - p1.y) / (p2.x - p1.x)
                        if abs(m) < 0.0000001:
                            if rect.bottom < p1.y < rect.top:
                                self.velocity.x = -self.velocity.x
                            else:
                                self.velocity.y = -self.velocity.y
                        else:
                            b = p2.y - m * p2.x
                            if p2.y < p1.y:  # we're below the obstacle
                                x = (rect.bottom - b) / m
                                if rect.left < x < rect.right:
                                    self.velocity.y = -self.velocity.y
                                else:
                                    self.velocity.x = -self.velocity.x
                            else:  # we're above the obstacle
                                x = (rect.top - b) / m
                                if rect.left < x < rect.right:
                                    self.velocity.y = -self.velocity.y
                                else:
                                    self.velocity.x = -self.velocity.x

                    self.pos = orig_pos + self.velocity * dt
                    self.rect.x = self.pos.x
                    self.rect.y = self.pos.y
                else:
                    self.kill()
                break


class ProjectileFactory:
    """
    Factory class for projectiles.
    """

    def __init__(self, projectile_info):
        self.level = None
        self.image = projectile_info.image
        self.speed = projectile_info.speed
        self.damage = projectile_info.damage
        self.max_distance = projectile_info.max_distance
        self.bounce = projectile_info.bounce

    def create(self, pos, direction):
        if self.level is None:
            print("ERROR: ProjectileFactory.create(): not added to level yet")
            return

        velocity = pygame.Vector2(direction)
        if velocity.magnitude() > 0:
            velocity = velocity.normalize()
        velocity *= self.speed

        return Projectile(
            self.level,
            self.image,
            pos=pos,
            velocity=velocity,
            damage=self.damage,
            max_distance=self.max_distance,
            bounce=self.bounce)

    def add_to_level(self, level):
        self.level = level
