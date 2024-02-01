import pygame

class Animation:
    def __init__(self, images, rates):
        self.images = images
        self.rates = rates if isinstance(rates, list) else [rates] * len(images)
        if len(self.images) != len(self.rates):
            print("ERROR: animation images and rates are not the same length")
            if len(images) > len(rates):
                for _ in range(len(images) - len(rates)):
                    self.rates.append(self.rates[-1])
        self.ticks = pygame.time.get_ticks()
        self.index = 0
        self.ticks = None

    def update(self):
        if self.ticks is None:
            self.ticks = pygame.time.get_ticks()
        new_ticks = pygame.time.get_ticks()
        if (new_ticks - self.ticks) >= (self.rates[self.index] * 1000):
            self.ticks = new_ticks
            self.index = (self.index + 1) % len(self.images)
        return self.images[self.index]
