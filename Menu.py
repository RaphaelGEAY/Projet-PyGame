import pygame, sys
import Jeu
from Sons import play_menu_music, stop_menu_music, play_game_music, Shop_Game_music, play_boing_sound

pygame.init()

LARGEUR, HAUTEUR = 1200, 700
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Speed Run - Menu Principal")

fond_menu = pygame.image.load("Menus/Fond_menu.png")
fond_menu = pygame.transform.scale(fond_menu, (LARGEUR, HAUTEUR))
fond_boutique = pygame.image.load("Menus/Shop_menu.png")
fond_boutique = pygame.transform.scale(fond_boutique, (LARGEUR, HAUTEUR))

titre_image = pygame.image.load("Menus/SPEED_RUN.png")
rect_titre = titre_image.get_rect(center=(LARGEUR / 2, 70))

img_jouer = pygame.image.load("Menus/START.png").convert_alpha()
img_boutique = pygame.image.load("Menus/Shop.png").convert_alpha()
img_quitter = pygame.image.load("Menus/QUIT.png").convert_alpha()
img_options = pygame.image.load("Menus/Settings.png").convert_alpha()

taille_jouer = (260, 190)
taille_quitter = (260, 200)
taille_boutique = (270, 250)
taille_options = (180, 180)

img_jouer = pygame.transform.scale(img_jouer, taille_jouer)
img_quitter = pygame.transform.scale(img_quitter, taille_quitter)
img_boutique = pygame.transform.scale(img_boutique, taille_boutique)
img_options = pygame.transform.scale(img_options, taille_options)

rect_jouer = img_jouer.get_rect(center=(LARGEUR // 2, 250))
rect_boutique = img_boutique.get_rect(center=(LARGEUR // 2, 405))
rect_quitter = img_quitter.get_rect(center=(LARGEUR // 2, 560))
rect_options = img_options.get_rect(center=(LARGEUR - 120, 500))

def dessiner_bouton_pop(image, taille_base, rect, facteur=1.2):
    souris = pygame.mouse.get_pos()
    if rect.collidepoint(souris):
        nouvelle_taille = (int(taille_base[0] * facteur), int(taille_base[1] * facteur))
        image_redim = pygame.transform.scale(image, nouvelle_taille)
        nouveau_rect = image_redim.get_rect(center=rect.center)
        ecran.blit(image_redim, nouveau_rect)
    else:
        ecran.blit(image, rect)

def quitter_jeu():
	pygame.quit()
	sys.exit()

def menu_boutique():
    stop_menu_music()      # Arrête la musique du menu
    Shop_Game_music()      # Lance la musique de la boutique
    while True:
        ecran.blit(fond_boutique, (0, 0))
        police_retour = pygame.font.Font(None, 60)
        texte_retour = police_retour.render("Retour", True, (255, 255, 255))
        rect_retour = texte_retour.get_rect(center=(100, 50))
        ecran.blit(texte_retour, rect_retour)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_menu_music()
                quitter_jeu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retour.collidepoint(event.pos):
                    stop_menu_music()      # Arrête la musique de la boutique
                    play_menu_music()      # Relance la musique du menu
                    return
        pygame.display.update()

def menu_options():
	print("Menu des options (à compléter)")

def lancer_jeu():
    stop_menu_music()      # Arrête la musique du menu
    play_game_music()      # Lance la musique du jeu
    Jeu.lancer_jeu(retour_menu=menu_principal)

def menu_principal():
    play_menu_music()
    while True:
        ecran.blit(fond_menu, (0, 0))
        ecran.blit(titre_image, rect_titre)
        dessiner_bouton_pop(img_jouer, taille_jouer, rect_jouer, 1.2)
        dessiner_bouton_pop(img_boutique, taille_boutique, rect_boutique, 1.2)
        dessiner_bouton_pop(img_quitter, taille_quitter, rect_quitter, 1.2)
        dessiner_bouton_pop(img_options, taille_options, rect_options, 1.2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_menu_music()
                quitter_jeu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_jouer.collidepoint(event.pos):
                    play_boing_sound()
                    pygame.time.wait(150)
                    lancer_jeu()
                elif rect_boutique.collidepoint(event.pos):
                    play_boing_sound()
                    pygame.time.wait(150)
                    menu_boutique()
                elif rect_quitter.collidepoint(event.pos):
                    play_boing_sound()
                    pygame.time.wait(150)
                    quitter_jeu()
                elif rect_options.collidepoint(event.pos):
                    play_boing_sound()
                    pygame.time.wait(150)
                    menu_options()

        pygame.display.update()

menu_principal()
