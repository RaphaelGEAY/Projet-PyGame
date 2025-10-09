# GestionObstacles.py
import random
import pygame

from Obstacles.VoitureBleue import VoitureBleue
from Obstacles.VoitureNoire import VoitureNoire
from Obstacles.VoitureOrange import VoitureOrange
from Obstacles.VoitureViolet import VoitureViolet
from Obstacles.VoitureJaune import VoitureJaune
from Obstacles.Herse import Herse
from Obstacles.Boost import Boost
from Obstacles.Pneus import Pneus
from Obstacles.Obstacle import Obstacle  # fallback / "simple" obstacle


class GestionObstacles:
    """
    Gestion centralisée des obstacles :
    - spawn (probabilités configurées ici)
    - mise à jour (déplacement + zigzag)
    - nettoyage hors écran
    - dessin (chaque obstacle dessine sa propre image)
    """

    def __init__(self, route, intervalle=18):
        """
        route : instance de Route (doit exposer x_route, largeur_route)
        intervalle : cadence de spawn (nombre de tick entre spawns)
        """
        self.route = route
        self.liste = []
        self.compteur = 0
        self.intervalle = intervalle

    def gerer_spawn(self):
        """Incrémente le compteur et spawn quand nécessaire."""
        self.compteur += 1
        if self.compteur >= self.intervalle:
            self.creer_obstacle()
            self.compteur = 0

    def creer_obstacle(self):
        """
        Choisit un type d'obstacle et l'ajoute à la liste.
        Probabilités ajustables ici.
        """
        types = ["herse", "boost", "bleue", "noire", "orange", "violet", "jaune", "pneus"]
        poids =  [0.01,      0.02,     0.12,     0.12,      0.05,      0.05,      0.05,     0.5]

        type_obs = random.choices(types, weights=poids, k=1)[0]

        # y de spawn (au dessus de l'écran)
        if type_obs == "herse":
            # placer la herse plutôt vers le centre (comme avant)
            x = self.route.x_route + (self.route.largeur_route // 2) - 110
            y = -150
            obs = Herse(x, y)

        elif type_obs == "boost":
            cote = random.choice(["gauche", "droite"])
            y = -100
            if cote == "gauche":
                x = self.route.x_route + 20
            else:
                x = self.route.x_route + self.route.largeur_route - 120
            obs = Boost(x, y)

        elif type_obs == "pneus":
            # spawn pneus plutôt en bord de route, légèrement aléatoire
            y = -80
            cote = random.choice(["gauche", "centre", "droite"])
            if cote == "gauche":
                x = self.route.x_route + 40
            elif cote == "droite":
                x = self.route.x_route + self.route.largeur_route - 100
            else:  # centre
                x = self.route.x_route + (self.route.largeur_route // 2) - 30
            # On suppose que Obstacles/Pneus.py définit class Pneus(Obstacle) avec __init__(x, y)
            obs = Pneus(x, y)
        else:
            # voitures colorées
            x = random.randint(self.route.x_route, self.route.x_route + self.route.largeur_route - 50)
            y = -100
            mapping = {
                "bleue": VoitureBleue,
                "noire": VoitureNoire,
                "orange": VoitureOrange,
                "violet": VoitureViolet,
                "jaune": VoitureJaune
            }
            cls = mapping.get(type_obs, VoitureBleue)
            obs = cls(x, y)

        # propriétés auxiliaires pour mouvement fluide / zigzag
        if not hasattr(obs, "zigzag"):
            obs.zigzag = (random.random() < 0.25)
            obs.zigzag_speed = random.choice([-2, 2]) if obs.zigzag else 0

        if not hasattr(obs, "y_precise"):
            # stocker une position y en float (pour déplacements doux)
            # certaines classes peuvent déjà avoir y_precise; si non -> on la crée
            obs.y_precise = float(obs.rect.y)

        self.liste.append(obs)

    def mettre_a_jour(self, vitesse):
        """
        Déplace les obstacles selon 'vitesse' (float/int).
        Gère également le zigzag horizontal (avec bornes sur la route).
        """
        for obs in self.liste:
            # déplacement vertical lisse en float
            obs.y_precise += vitesse
            try:
                obs.rect.y = int(obs.y_precise)
            except Exception:
                # si l'objet n'a pas rect (improbable), ignorer
                continue

            # zigzag horizontal
            if getattr(obs, "zigzag", False):
                obs.rect.x += obs.zigzag_speed
                # clamp sur les bords de la route
                if obs.rect.x < self.route.x_route:
                    obs.rect.x = self.route.x_route
                    obs.zigzag_speed *= -1
                if obs.rect.x + obs.rect.width > self.route.x_route + self.route.largeur_route:
                    obs.rect.x = self.route.x_route + self.route.largeur_route - obs.rect.width
                    obs.zigzag_speed *= -1

    def nettoyer(self, hauteur):
        """Enlève les obstacles qui sont passés sous 'hauteur' (bas de l'écran)."""
        self.liste = [obs for obs in self.liste if obs.rect.y < hauteur]

    def dessiner(self, ecran):
        """Délègue le dessin à chaque obstacle (méthode draw)."""
        for obs in self.liste:
            # préférence pour obs.draw si disponible
            draw_fn = getattr(obs, "draw", None)
            if callable(draw_fn):
                draw_fn(ecran)
            else:
                # fallback : essayer blit sur image, sinon rect
                if getattr(obs, "image", None) is not None:
                    ecran.blit(obs.image, obs.rect)
                else:
                    pygame.draw.rect(ecran, getattr(obs, "couleur", (255, 0, 255)), obs.rect)
