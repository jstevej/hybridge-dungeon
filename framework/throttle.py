import pygame

class ThrottleEvent:
    def __init__(self, rate):
        self._rate = rate * 1000
        self.ticks = pygame.time.get_ticks()

    @property
    def rate(self):
        return self._rate / 1000

    @rate.setter
    def rate(self, value):
        self._rate = value * 1000

    def update(self):
        new_ticks = pygame.time.get_ticks()
        if (new_ticks - self.ticks) >= self._rate:
            self.ticks = new_ticks
            return True
        return False

class ThrottleValue:
    def __init__(self, rate, initial_value):
        self.rate = rate
        self._value = initial_value
        self.ticks = pygame.time.get_ticks()

    @property
    def rate(self):
        return self._rate / 1000

    @rate.setter
    def rate(self, value):
        self._rate = value * 1000

    def update(self, value):
        new_ticks = pygame.time.get_ticks()
        if new_ticks - self.ticks >= self._rate:
            self.ticks = new_ticks
            self._value = value
        return self._value

    @property
    def value(self):
        return self._value
