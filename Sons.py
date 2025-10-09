import pygame

if not pygame.mixer.get_init():
    pygame.mixer.init()

def play_menu_music():
    pygame.mixer.music.load(r"Assets\Sons\Musiques\Musique_salon.wav")
    pygame.mixer.music.play(-1)

def play_game_music():
    pygame.mixer.music.load(r"Assets\Sons\Musiques\Musique_combat.wav")
    pygame.mixer.music.play(-1)

def Shop_Game_music():
    pygame.mixer.music.load(r"Assets\Sons\Musiques\Musique_game.wav")
    pygame.mixer.music.play(-1)

def stop_menu_music():
    pygame.mixer.music.stop()

def play_crash_sound():
    pygame.mixer.music.stop()
    crash_sound = pygame.mixer.Sound(r"Assets\Sons\Effets\Car_crash_sound.mp3")
    crash_sound.play()

def play_boing_sound():
    boing = pygame.mixer.Sound(r"Assets\Sons\Effets\Boing.mp3")
    boing.play()
