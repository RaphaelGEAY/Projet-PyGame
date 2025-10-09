import pygame
from Obstacles.Obstacle import Obstacle

class Boost(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 150, 150, (180, 180, 60))
        self.image = pygame.image.load(r"assets/Item/Boost.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(topleft=(x, y))
