# Jeu.py
import pygame
import sys

from GestionScore import GestionScore
from GestionObstacles import GestionObstacles
from Route import Route

# Obstacles spécifiques utilisés pour la logique (Herse & Boost & Pneus si besoin pour isinstance)
try:
    from Obstacles.Herse import Herse
except Exception:
    Herse = None

try:
    from Obstacles.Boost import Boost
except Exception:
    Boost = None

# Sons (tolérant)
try:
    from Sons import play_crash_sound, play_game_music
except Exception:
    def play_crash_sound(): pass
    def play_game_music(): pass

# Décors (tolérant)
try:
    from Decors.Plaine import Plaine
    from Decors.Desert import Desert
    from Decors.Neige import Neige
    from Decors.Volcan import Volcan
    from Decors.Galaxie import Galaxie
    _DECORS_OK = True
except Exception:
    _DECORS_OK = False

# Véhicules (import explicite — si tu rajoutes d'autres fichiers, ajoute-les ici)
_veh_classes = []
try:
    from Vehicules.VoitureDeBase import VoitureDeBase; _veh_classes.append(VoitureDeBase)
except Exception: pass
try:
    from Vehicules.VoitureDeCourse import VoitureDeCourse; _veh_classes.append(VoitureDeCourse)
except Exception: pass
try:
    from Vehicules.Fourgon import Fourgon; _veh_classes.append(Fourgon)
except Exception: pass
try:
    from Vehicules.Moto import Moto; _veh_classes.append(Moto)
except Exception: pass
try:
    from Vehicules.Velo import Velo; _veh_classes.append(Velo)
except Exception: pass

# Fallback véhicule si aucune classe trouvée
if not _veh_classes:
    class _FallbackVehicule:
        def __init__(self):
            self.name = "Fallback"
            self.image = None
        def deplacement_h(self): return 5
        def boost(self): return 0
    _veh_classes = [_FallbackVehicule]


class Jeu:
    def __init__(self, retour_menu=None):
        pygame.init()
        self.largeur, self.hauteur = 1200, 700
        self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("SPEED RUN")

        # UI colors
        self.vert = (34, 139, 34)
        self.blanc = (255, 255, 255)
        self.bleu = (0, 120, 215)
        self.gris_fonce = (60, 60, 60)

        # véhicules
        self.vehicules = [cls() for cls in _veh_classes]
        # label lisible pour UI : si 'name' existe sur l'instance, sinon nom de classe
        self.noms_vehicules = [getattr(v, "name", v.__class__.__name__) for v in self.vehicules]

        self.index_vehicule = 0
        self.vehicule = self.vehicules[self.index_vehicule]
        self.texture_actuelle = getattr(self.vehicule, "image", None)

        # voiture size (si image fournie, on s'aligne dessus)
        if self.texture_actuelle:
            try:
                w, h = self.texture_actuelle.get_size()
                self.voiture_largeur, self.voiture_hauteur = w, h
            except Exception:
                self.voiture_largeur, self.voiture_hauteur = 40, 80
        else:
            self.voiture_largeur, self.voiture_hauteur = 40, 80

        self.voiture_x = self.largeur // 2 - self.voiture_largeur // 2
        self.voiture_y = self.hauteur - self.voiture_hauteur - 30

        # route & obstacles
        self.route = Route(self.largeur, self.hauteur)
        self.gestion_obstacles = GestionObstacles(self.route)

        # horloge & polices
        self.horloge = pygame.time.Clock()
        self.police = pygame.font.SysFont(None, 48)
        self.police_score = pygame.font.SysFont(None, 36)
        self.police_bouton = pygame.font.SysFont(None, 28)

        # état jeu
        self.partie_terminee = False
        self.score = 0
        self.vitesse_base_obstacles = 7.0
        self.vitesse_globale = self.vitesse_base_obstacles
        self.decalage_boost = 0
        self.gestion_score = GestionScore()
        self.retour_menu = retour_menu
        self.timer_boost_pad = 0

        # décors
        if _DECORS_OK:
            self.decors = [Plaine(), Desert(), Neige(), Volcan(), Galaxie()]
        else:
            self.decors = []
        self.index_decor = 0
        self.decor_actuel = self.decors[self.index_decor] if self.decors else None

        # NOTE: musique lancée par le menu ; si tu veux lancer ici, décommente next lines:
        # try: play_game_music()
        # except: pass

    def changer_decor(self):
        if not self.decors:
            return
        self.index_decor = (self.index_decor + 1) % len(self.decors)
        self.decor_actuel = self.decors[self.index_decor]

    def redemarrer(self):
        self.voiture_x = self.largeur // 2 - self.voiture_largeur // 2
        self.gestion_obstacles.liste = []
        self.score = 0
        self.timer_boost_pad = 0
        self.partie_terminee = False
        self.vitesse_globale = self.vitesse_base_obstacles
        self.index_decor = 0
        if self.decors:
            self.decor_actuel = self.decors[self.index_decor]
        try:
            play_game_music()
        except Exception:
            pass

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
                        # change vehicle
                        self.index_vehicule = (self.index_vehicule + 1) % len(self.vehicules)
                        self.vehicule = self.vehicules[self.index_vehicule]
                        self.texture_actuelle = getattr(self.vehicule, "image", None)
                        if self.texture_actuelle:
                            try:
                                w, h = self.texture_actuelle.get_size()
                                self.voiture_largeur, self.voiture_hauteur = w, h
                            except Exception:
                                self.voiture_largeur, self.voiture_hauteur = 40, 80
                        self.voiture_x = self.largeur // 2 - self.voiture_largeur // 2

            # boost vertical effect (up key)
            decalage_max = 60
            vitesse_monte = 4
            vitesse_descend = 3
            boost_actif = False

            if not self.partie_terminee:
                if touches[pygame.K_UP]:
                    if self.decalage_boost < decalage_max:
                        self.decalage_boost += vitesse_monte
                    boost_actif = True
                else:
                    if self.decalage_boost > 0:
                        self.decalage_boost -= vitesse_descend

            if not self.partie_terminee:
                # déplacements horizontaux via la méthode de la classe véhicule
                move_fn = getattr(self.vehicule, "deplacement_h", None)
                if touches[pygame.K_LEFT]:
                    if callable(move_fn):
                        try: self.voiture_x -= move_fn()
                        except Exception: self.voiture_x -= 5
                    else:
                        self.voiture_x -= 5
                if touches[pygame.K_RIGHT]:
                    if callable(move_fn):
                        try: self.voiture_x += move_fn()
                        except Exception: self.voiture_x += 5
                    else:
                        self.voiture_x += 5

                # limiter la position sur la route
                try:
                    self.route.limiter_position(self)
                except Exception:
                    # fallback simple
                    if self.voiture_x < 0: self.voiture_x = 0
                    if self.voiture_x + self.voiture_largeur > self.largeur: self.voiture_x = self.largeur - self.voiture_largeur

                # spawn & update obstacles
                self.gestion_obstacles.gerer_spawn()

                augmentation_temps = self.score / 120.0
                vitesse_base = self.vitesse_base_obstacles + augmentation_temps

                if self.timer_boost_pad > 0:
                    self.timer_boost_pad -= 1
                    vitesse_base += 6

                # récupération boost du véhicule (méthode ou attribut)
                boost_val = 0
                b = getattr(self.vehicule, "boost", None)
                if callable(b):
                    try: boost_val = b()
                    except Exception: boost_val = 0
                else:
                    try: boost_val = int(getattr(self.vehicule, "boost", 0))
                    except Exception: boost_val = 0

                if boost_actif:
                    self.vitesse_globale = vitesse_base + boost_val
                else:
                    self.vitesse_globale = vitesse_base

                self.gestion_obstacles.mettre_a_jour(self.vitesse_globale)

                # box de collision
                marge_x = 10
                marge_y = 10
                rect_voiture = pygame.Rect(
                    self.voiture_x + marge_x,
                    self.voiture_y - self.decalage_boost + marge_y,
                    max(1, self.voiture_largeur - 2 * marge_x),
                    max(1, self.voiture_hauteur - 2 * marge_y)
                )

                # collisions
                for obs in list(self.gestion_obstacles.liste):
                    # si herse et boost actif -> on passe à travers (comportement voulu)
                    if Herse is not None and isinstance(obs, Herse) and boost_actif:
                        continue
                    # boost pad detection
                    if Boost is not None and isinstance(obs, Boost) and rect_voiture.colliderect(getattr(obs, "rect", pygame.Rect(0,0,0,0))):
                        self.timer_boost_pad = 12
                        continue
                    # collision générale
                    if rect_voiture.colliderect(getattr(obs, "rect", pygame.Rect(0,0,0,0))):
                        self.partie_terminee = True
                        try:
                            play_crash_sound()
                        except Exception:
                            pass
                        break

                self.gestion_obstacles.nettoyer(self.hauteur)
                self.score += 1

                # changement décor tous les 400 pts
                if self.decors and self.score % 400 == 0:
                    self.changer_decor()

            # DESSIN
            # décor
            if self.decor_actuel:
                try:
                    self.decor_actuel.draw(self.ecran)
                except Exception:
                    self.ecran.fill(self.vert)
            else:
                self.ecran.fill(self.vert)

            # route
            try:
                self.route.dessiner(self.ecran, self.vitesse_globale, self.partie_terminee)
            except Exception:
                pygame.draw.rect(self.ecran, (120, 120, 120), (self.route.x_route, 0, self.route.largeur_route, self.hauteur))

            # obstacles (GestionObstacles dessine les si chaque obstacle a draw)
            try:
                self.gestion_obstacles.dessiner(self.ecran)
            except TypeError:
                try:
                    self.gestion_obstacles.dessiner(self.ecran, {})
                except Exception:
                    pass

            # voiture (image ou rectangle)
            voiture_y_aff = self.voiture_y - self.decalage_boost
            if self.texture_actuelle:
                try:
                    self.ecran.blit(self.texture_actuelle, (self.voiture_x, voiture_y_aff))
                except Exception:
                    pygame.draw.rect(self.ecran, (200, 0, 0), (self.voiture_x, voiture_y_aff, self.voiture_largeur, self.voiture_hauteur))
            else:
                pygame.draw.rect(self.ecran, (200, 0, 0), (self.voiture_x, voiture_y_aff, self.voiture_largeur, self.voiture_hauteur))

            # UI
            score_txt = self.police_score.render(f"Score : {self.score}", True, (0, 0, 0))
            self.ecran.blit(score_txt, (20, 70))
            high_txt = self.police_score.render(f"Record : {self.gestion_score.meilleur_score}", True, (0, 0, 0))
            self.ecran.blit(high_txt, (20, 100))

            # boutons
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

            # Game Over
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

            # clics souris
            for event in evenements:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if changer_rect.collidepoint(event.pos):
                        self.index_vehicule = (self.index_vehicule + 1) % len(self.vehicules)
                        self.vehicule = self.vehicules[self.index_vehicule]
                        self.texture_actuelle = getattr(self.vehicule, "image", None)
                        if self.texture_actuelle:
                            try:
                                w, h = self.texture_actuelle.get_size()
                                self.voiture_largeur, self.voiture_hauteur = w, h
                            except Exception:
                                self.voiture_largeur, self.voiture_hauteur = 40, 80
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
