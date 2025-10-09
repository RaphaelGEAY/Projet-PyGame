import pygame, sys
import Jeu
from SoundPrincipal import play_menu_music, stop_menu_music, play_game_music, Shop_Game_music, play_boing_sound

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

taille_jouer = (260, 140)
taille_quitter = (230, 120)
taille_boutique = (265, 130)
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
    stop_menu_music()
    Shop_Game_music()

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
                    stop_menu_music()
                    play_menu_music()
                    return

        pygame.display.update()

def menu_options():
    global sound_on
    sound_on = True 

    sound_on_img = pygame.image.load("Menus/sound_on_img.png").convert_alpha()
    sound_off_img = pygame.image.load("Menus/sound_off_img.png").convert_alpha()

    taille_son = (100, 100)
    sound_on_img = pygame.transform.scale(sound_on_img, taille_son)
    sound_off_img = pygame.transform.scale(sound_off_img, taille_son)

    rect_son = sound_on_img.get_rect(center=(LARGEUR / 2 + 150, 300))

    stop_menu_music()  

    while True:
        ecran.fill((25, 25, 35))

        # Titre
        police_titre = pygame.font.Font(None, 100)
        texte_titre = police_titre.render("OPTIONS", True, (255, 255, 255))
        rect_titre_opt = texte_titre.get_rect(center=(LARGEUR / 2, 100))
        ecran.blit(texte_titre, rect_titre_opt)

        police_volume = pygame.font.Font(None, 60)
        texte_volume = police_volume.render("Volume :", True, (200, 200, 200))
        ecran.blit(texte_volume, (LARGEUR / 2 - 200, 280))

        if sound_on:
            ecran.blit(sound_on_img, rect_son)
        else:
            ecran.blit(sound_off_img, rect_son)

        police_retour = pygame.font.Font(None, 60)
        texte_retour = police_retour.render("Retour", True, (255, 255, 255))
        rect_retour = texte_retour.get_rect(center=(100, 50))
        ecran.blit(texte_retour, rect_retour)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter_jeu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retour.collidepoint(event.pos):
                    if sound_on:
                        play_menu_music()  
                    return

                if rect_son.collidepoint(event.pos):
                    sound_on = not sound_on
                    if sound_on:
                        play_menu_music()
                        print("🔊 Son activé")
                    else:
                        stop_menu_music()
                        print("🔇 Son coupé")

        pygame.display.update()

def lancer_jeu():
    stop_menu_music()
    play_game_music()
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
