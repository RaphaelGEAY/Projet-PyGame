import pygame
import os

class Vehicule:
    """
    Classe de base pour tous les véhicules.
    Gère la vitesse, le boost et la texture.
    """

    def __init__(self, image_nom, vitesseH, vitesseV, multiplicateur):
        self.vitesse_h = vitesseH
        self.vitesse_v = vitesseV
        self.multiplicateur = multiplicateur

        # 🔹 Chargement de la texture
        chemin = os.path.join("Assets", "Textures", "Vehicules", image_nom)
        if os.path.exists(chemin):
            self.image = pygame.image.load(chemin).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 80))
        else:
            print(f"[ERREUR] Image de véhicule introuvable : {chemin}")
            self.image = pygame.Surface((40, 80))
            self.image.fill((255, 0, 0))

    def deplacement_h(self):
        """Vitesse de déplacement horizontal."""
        return self.vitesse_h

    def boost(self):
        """Retourne le bonus de vitesse vertical."""
        return self.vitesse_v * self.multiplicateur
