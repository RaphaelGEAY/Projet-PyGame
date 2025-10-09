import pygame
import os

class Decor:
    """
    Classe de base pour les décors du jeu.
    Chaque sous-classe définit simplement le nom de son image.
    """

    def __init__(self, image_nom):
        chemin = os.path.join("Assets", "Textures", "Decors", image_nom)
        if os.path.exists(chemin):
            self.image = pygame.image.load(chemin).convert()
            self.image = pygame.transform.scale(self.image, (1200, 700))
        else:
            print(f"[ERREUR] Image de décor introuvable : {chemin}")
            self.image = None

    def draw(self, ecran):
        """Affiche le décor sur l’écran de jeu."""
        if self.image:
            ecran.blit(self.image, (0, 0))
        else:
            ecran.fill((0, 0, 0))  # fond noir par défaut si image absente
