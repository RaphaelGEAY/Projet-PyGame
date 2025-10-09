import pygame

if not pygame.mixer.get_init():
    pygame.mixer.init()

def play_menu_music():
    pygame.mixer.music.load(r"C:\Users\rodne\Documents\Projet-PyGame\assets\Sound\Soundprincipal\Musique Salon.wav")
    pygame.mixer.music.play(-1)

def play_game_music():
    pygame.mixer.music.load(r"C:\Users\rodne\Documents\Projet-PyGame\assets\Sound\Soundprincipal\Musique Combat.wav")
    pygame.mixer.music.play(-1)

def Shop_Game_music():
    pygame.mixer.music.load(r"C:\Users\rodne\Documents\Projet-PyGame\assets\Sound\Soundprincipal\Musique Game.wav")
    pygame.mixer.music.play(-1)

def stop_menu_music():
    pygame.mixer.music.stop()

def play_crash_sound():
    pygame.mixer.music.stop()  # Arrête la musique en cours
    crash_sound = pygame.mixer.Sound(r"C:\Users\rodne\Documents\Projet-PyGame\assets\Sound\Sound effect\car-crash-sound.mp3")
    crash_sound.play()

def play_boing_sound():
    boing = pygame.mixer.Sound(r"C:\Users\rodne\Documents\Projet-PyGame\assets\Sound\Sound effect\boing.mp3")
    boing.play()