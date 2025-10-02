import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interface Pygame")

# Définir les couleurs
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)

# Boucle principale
running = True
while running:
    button_rect = pygame.Rect(350, 250, 100, 50)
    button_color = BLUE
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # Changement de couleur au survol
    if button_rect.collidepoint(mouse_pos):
        if mouse_pressed:
            button_color = (0, 80, 150)  # Couleur lors du clic
        else:
            button_color = (0, 180, 255)  # Couleur lors du survol

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Bouton Jouer cliqué !")

    screen.fill(WHITE)

    # Exemple d'interface : un bouton
    pygame.draw.rect(screen, button_color, button_rect)
    
    # Texte sur le bouton
    font = pygame.font.SysFont(None, 36)
    text = font.render("Jouer", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()