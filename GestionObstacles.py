import random
from Obstacles.VoitureBleue import VoitureBleue
from Obstacles.VoitureNoire import VoitureNoire
from Obstacles.VoitureOrange import VoitureOrange
from Obstacles.VoitureViolet import VoitureViolet
from Obstacles.VoitureJaune import VoitureJaune
from Obstacles.BarrierePolice import BarrierePolice
from Obstacles.Boost import Boost
from Obstacles.Obstacle import Obstacle

class GestionObstacles:
	def __init__(self, route):
		self.route = route
		self.liste = []
		self.compteur = 0
		self.intervalle = 18

	def gerer_spawn(self):
		self.compteur += 1
		if self.compteur >= self.intervalle:
			self.creer_obstacle()
			self.compteur = 0

	def creer_obstacle(self):
		type_obs = random.choices(
			["barriere", "boost", "bleue", "noire", "orange", "violet", "jaune", "simple"],
			weights=[0.01, 0.02, 0.12, 0.12, 0.05, 0.05, 0.05, 0.58],
			k=1
		)[0]
		if type_obs == "barriere":
			x = self.route.x_route + (self.route.largeur_route // 2) - 110
			y = -150
			obs = BarrierePolice(x, y)
		elif type_obs == "boost":
			cote = random.choice(["gauche", "droite"])
			y = -100
			if cote == "gauche":
				x = self.route.x_route + 20
			else:
				x = self.route.x_route + self.route.largeur_route - 120
			obs = Boost(x, y)
		elif type_obs == "simple":
			w = random.randint(30, 70)
			h = random.randint(30, 60)
			x = random.randint(self.route.x_route, self.route.x_route + self.route.largeur_route - w)
			obs = Obstacle(x, -h, w, h, random.choice([(0,0,0),(0,120,215),(255,140,0),(128,0,128)]))
		else:
			x = random.randint(self.route.x_route, self.route.x_route + self.route.largeur_route - 50)
			y = -100
			classe = {"bleue": VoitureBleue, "noire": VoitureNoire, "orange": VoitureOrange, "violet": VoitureViolet, "jaune": VoitureJaune}[type_obs]
			obs = classe(x, y)
		if not hasattr(obs, "zigzag"):
			obs.zigzag = (random.random() < 0.25)
			obs.zigzag_speed = random.choice([-2,2]) if obs.zigzag else 0
		if not hasattr(obs, "y_precise"):
			obs.y_precise = float(obs.rect.y)
		self.liste.append(obs)

	def mettre_a_jour(self, vitesse):
		for obs in self.liste:
			obs.y_precise += vitesse
			obs.rect.y = int(obs.y_precise)
			if getattr(obs, "zigzag", False):
				obs.rect.x += obs.zigzag_speed
				if obs.rect.x < self.route.x_route:
					obs.rect.x = self.route.x_route
					obs.zigzag_speed *= -1
				if obs.rect.x + obs.rect.width > self.route.x_route + self.route.largeur_route:
					obs.rect.x = self.route.x_route + self.route.largeur_route - obs.rect.width
					obs.zigzag_speed *= -1

	def nettoyer(self, hauteur):
		self.liste = [obs for obs in self.liste if obs.rect.y < hauteur]

	def dessiner(self, ecran):
		for obs in self.liste:
			obs.draw(ecran)
