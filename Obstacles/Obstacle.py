import pygame
import os

class Obstacle:
    """
    Classe de base pour les obstacles.
    Gère l’image, la position et le déplacement vertical.
    """

    def __init__(self, image_nom, x, y, largeur, hauteur):
        chemin = os.path.join("Assets", "Textures", "Obstacles", image_nom)
        if os.path.exists(chemin):
            self.image = pygame.image.load(chemin).convert_alpha()
            self.image = pygame.transform.scale(self.image, (largeur, hauteur))
        else:
            print(f"[ERREUR] Image d'obstacle introuvable : {chemin}")
            self.image = pygame.Surface((largeur, hauteur))
            self.image.fill((255, 0, 0))  # rouge si image manquante

        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, vitesse):
        """Déplace l’obstacle vers le bas."""
        self.rect.y += vitesse

    def draw(self, ecran):
        """Affiche l’obstacle."""
        ecran.blit(self.image, self.rect)
