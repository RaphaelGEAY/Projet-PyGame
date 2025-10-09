import pygame
from Vehicules.Vehicule import Vehicule

class VoitureDeBase(Vehicule):
    def __init__(self, skin_path="assets/Skins/voiture/PlayerCar1.png"):
        super().__init__(vitesseH=5, vitesseV=5, multiplicateur=1.0)
        self.skin_path = skin_path
        self.image = pygame.image.load(self.skin_path).convert_alpha()
        self.rect = self.image.get_rect()

    def set_skin(self, skin_path):
        self.skin_path = skin_path
        self.image = pygame.image.load(self.skin_path).convert_alpha()
        self.rect = self.image.get_rect()
