import pygame

class Obstacle:
	def __init__(self, x, y, largeur, hauteur, couleur):
		self.rect = pygame.Rect(x, y, largeur, hauteur)
		self.couleur = couleur

	def draw(self, ecran):
		pygame.draw.rect(ecran, self.couleur, self.rect)
		
	def update(self, vitesse):
		self.rect.y += vitesse
