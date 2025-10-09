import pygame

class Route:
	def __init__(self, largeur, hauteur):
		self.largeur = largeur
		self.hauteur = hauteur
		self.largeur_route = 380
		self.x_route = self.largeur // 2 - self.largeur_route // 2
		self.decalage = 0
		self.cote = 8

	def limiter_position(self, jeu):
		if jeu.voiture_x < self.x_route:
			jeu.voiture_x = self.x_route
		if jeu.voiture_x + jeu.voiture_largeur > self.x_route + self.largeur_route:
			jeu.voiture_x = self.x_route + self.largeur_route - jeu.voiture_largeur

	def dessiner(self, ecran, vitesse, partie_terminee=False):
		pygame.draw.rect(ecran, (180, 180, 180), (self.x_route, 0, self.largeur_route, self.hauteur))
		pygame.draw.rect(ecran, (255, 255, 255), (self.x_route + 12, 0, self.cote, self.hauteur))
		pygame.draw.rect(ecran, (255, 255, 255), (self.x_route + self.largeur_route - 12 - self.cote, 0, self.cote, self.hauteur))

		if not partie_terminee:
			self.decalage = (self.decalage + vitesse) % 40

		for i in range(-40, self.hauteur + 40, 40):
			pygame.draw.rect(ecran, (255, 255, 255), (self.largeur // 2 - 5, i + int(self.decalage), 10, 30))
