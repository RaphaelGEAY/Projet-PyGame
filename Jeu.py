import pygame, sys
from GestionScore import GestionScore
from GestionObstacles import GestionObstacles
from Route import Route
from Vehicules.VoitureDeBase import VoitureDeBase
from Vehicules.VoitureDeCourse import VoitureDeCourse
from Vehicules.Fourgon import Fourgon
from Vehicules.Moto import Moto
from Vehicules.Velo import Velo
from Obstacles.BarrierePolice import BarrierePolice
from Obstacles.Boost import Boost

class Jeu:
	def __init__(self, retour_menu=None):
		pygame.init()
		self.largeur, self.hauteur = 1200, 700
		self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
		pygame.display.set_caption("SPEED RUN")
		self.vert = (34, 139, 34)
		self.gris = (120, 120, 120)
		self.blanc = (255, 255, 255)
		self.rouge = (200, 0, 0)
		self.bleu = (0, 120, 215)
		self.gris_fonce = (60, 60, 60)
		self.vehicules = [VoitureDeBase(), VoitureDeCourse(), Fourgon(), Moto(), Velo()]
		self.noms_vehicules = ["Voiture de base", "Voiture de course", "Fourgon", "Moto", "Vélo"]
		self.index_vehicule = 0
		self.vehicule = self.vehicules[self.index_vehicule]
		self.voiture_largeur, self.voiture_hauteur = 40, 60
		self.voiture_x = self.largeur // 2 - self.voiture_largeur // 2
		self.voiture_y = self.hauteur - self.voiture_hauteur - 30
		self.route = Route(self.largeur, self.hauteur)
		self.gestion_obstacles = GestionObstacles(self.route)
		self.horloge = pygame.time.Clock()
		self.police = pygame.font.SysFont(None, 48)
		self.police_score = pygame.font.SysFont(None, 36)
		self.police_bouton = pygame.font.SysFont(None, 28)
		self.partie_terminee = False
		self.score = 0
		self.decalage_lignes = 0
		self.vitesse_base_obstacles = 7.0
		self.vitesse_globale = self.vitesse_base_obstacles
		self.offset_boost = 0
		self.gestion_score = GestionScore()
		self.retour_menu = retour_menu
		self.timer_boost_pad = 0

	def redemarrer(self):
		self.voiture_x = self.largeur // 2 - self.voiture_largeur // 2
		self.gestion_obstacles.liste = []
		self.score = 0
		self.timer_boost_pad = 0
		self.partie_terminee = False
		self.vitesse_globale = self.vitesse_base_obstacles
		self.decalage_lignes = 0

	def boucle(self):
		while True:
			evenements = pygame.event.get()
			restart_rect = None
			touches = pygame.key.get_pressed()
			for event in evenements:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if not self.partie_terminee and event.type == pygame.KEYDOWN:
					if event.key == pygame.K_TAB:
						self.index_vehicule = (self.index_vehicule + 1) % len(self.vehicules)
						self.vehicule = self.vehicules[self.index_vehicule]
						self.voiture_x = self.largeur // 2 - self.voiture_largeur // 2
			max_offset = 60
			vitesse_monte = 4
			vitesse_descend = 3
			boost_actif = False
			if not self.partie_terminee:
				if touches[pygame.K_SPACE]:
					if self.offset_boost < max_offset:
						self.offset_boost += vitesse_monte
					boost_actif = True
				else:
					if self.offset_boost > 0:
						self.offset_boost -= vitesse_descend
			if not self.partie_terminee:
				if touches[pygame.K_LEFT]:
					self.voiture_x -= self.vehicule.deplacement_h()
				if touches[pygame.K_RIGHT]:
					self.voiture_x += self.vehicule.deplacement_h()
				self.route.limiter_position(self)
				self.gestion_obstacles.gerer_spawn()
				self.gestion_obstacles.intervalle = self.gestion_obstacles.intervalle
				augmentation_temps = self.score / 120.0
				vitesse_base = self.vitesse_base_obstacles + augmentation_temps
				if self.timer_boost_pad > 0:
					self.timer_boost_pad -= 1
					vitesse_base += 6
				if boost_actif:
					self.vitesse_globale = vitesse_base + self.vehicule.boost()
				else:
					self.vitesse_globale = vitesse_base
				self.gestion_obstacles.mettre_a_jour(self.vitesse_globale)
				rect_voiture = pygame.Rect(self.voiture_x, self.voiture_y - self.offset_boost, self.voiture_largeur, self.voiture_hauteur)
				for obs in list(self.gestion_obstacles.liste):
					if isinstance(obs, BarrierePolice) and boost_actif:
						continue
					if isinstance(obs, Boost) and rect_voiture.colliderect(obs.rect):
						self.timer_boost_pad = 12
						continue
					if rect_voiture.colliderect(obs.rect):
						self.partie_terminee = True
				self.gestion_obstacles.nettoyer(self.hauteur)
				self.score += 1
			self.ecran.fill(self.vert)
			self.route.dessiner(self.ecran, self.vitesse_globale, self.partie_terminee)
			self.gestion_obstacles.dessiner(self.ecran)
			voiture_y_boost = self.voiture_y - self.offset_boost
			pygame.draw.rect(self.ecran, self.rouge, (self.voiture_x, voiture_y_boost, self.voiture_largeur, self.voiture_hauteur))
			score_txt = self.police_score.render(f"Score : {self.score}", True, (0, 0, 0))
			self.ecran.blit(score_txt, (20, 70))
			high_txt = self.police_score.render(f"Record : {self.gestion_score.meilleur_score}", True, (0, 0, 0))
			self.ecran.blit(high_txt, (20, 100))
			changer_rect = pygame.Rect(self.largeur - 200, 20, 180, 40)
			pygame.draw.rect(self.ecran, self.bleu, changer_rect)
			txt_change = self.police_bouton.render("Changer véhicule", True, self.blanc)
			self.ecran.blit(txt_change, txt_change.get_rect(center=changer_rect.center))
			menu_rect = pygame.Rect(20, 20, 120, 40)
			pygame.draw.rect(self.ecran, self.gris_fonce, menu_rect)
			txt_menu = self.police_bouton.render("Menu", True, self.blanc)
			self.ecran.blit(txt_menu, txt_menu.get_rect(center=menu_rect.center))
			txt_nom = self.police_bouton.render(f"Véhicule : {self.noms_vehicules[self.index_vehicule]}", True, (0, 0, 0))
			self.ecran.blit(txt_nom, (20, 150))
			if self.partie_terminee:
				if self.score > self.gestion_score.meilleur_score:
					self.gestion_score.mettre_a_jour(self.score)
				txt = self.police.render("Game Over!", True, (255, 0, 0))
				rect_txt = txt.get_rect(center=(self.largeur // 2, self.hauteur // 2 - 40))
				self.ecran.blit(txt, rect_txt)
				police_redemarrer = pygame.font.SysFont(None, 40)
				txt_redemarrer = police_redemarrer.render("Rejouer", True, self.blanc)
				restart_rect = pygame.Rect(self.largeur // 2 - 70, self.hauteur // 2 + 10, 140, 50)
				pygame.draw.rect(self.ecran, self.bleu, restart_rect)
				self.ecran.blit(txt_redemarrer, txt_redemarrer.get_rect(center=restart_rect.center))
			pygame.display.flip()
			self.horloge.tick(60)
			for event in evenements:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if changer_rect.collidepoint(event.pos):
						self.index_vehicule = (self.index_vehicule + 1) % len(self.vehicules)
						self.vehicule = self.vehicules[self.index_vehicule]
					elif menu_rect.collidepoint(event.pos):
						if self.retour_menu:
							self.retour_menu()
							return
						else:
							pygame.quit()
							sys.exit()
					elif self.partie_terminee and restart_rect and restart_rect.collidepoint(event.pos):
						self.redemarrer()

def lancer_jeu(retour_menu=None):
	jeu = Jeu(retour_menu)
	jeu.boucle()
