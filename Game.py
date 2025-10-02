import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 630
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu Example")

background = pygame.image.load("55492cea-b28c-4260-85cb-6b1210f78496.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

title_image = pygame.image.load("generated_text (1).png")
title_rect = title_image.get_rect(center=(WIDTH/2, 70))

start_img = pygame.image.load("START.png").convert_alpha()
quit_img = pygame.image.load("QUIT.png").convert_alpha()
settings_img = pygame.image.load("Settings.png").convert_alpha()

start_size = (260, 190)
quit_size = (260, 200)
settings_size = (270, 250)

start_img = pygame.transform.scale(start_img, start_size)
quit_img = pygame.transform.scale(quit_img, quit_size)
settings_img = pygame.transform.scale(settings_img, settings_size)

start_rect = start_img.get_rect(center=(WIDTH//2.01, 250))
quit_rect = quit_img.get_rect(center=(WIDTH//2, 560))
settings_rect = settings_img.get_rect(center=(WIDTH//2, 405))

def start_game():
    print("Game Started!")

def quit_game():
    pygame.quit()
    sys.exit()

def settings_game():
    print("You clicked on Settings")

def draw_pop_button(image, base_size, rect, scale_factor=1.2, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        new_size = (int(base_size[0] * scale_factor), int(base_size[1] * scale_factor))
        scaled_img = pygame.transform.scale(image, new_size)
        new_rect = scaled_img.get_rect(center=rect.center)
        screen.blit(scaled_img, new_rect)

        if click[0] == 1 and action is not None:
            action()
    else:
        screen.blit(image, rect)

def main_menu():
    while True:
        screen.blit(background, (0, 0))
        screen.blit(title_image, title_rect)

        draw_pop_button(start_img, start_size, start_rect, 1.2, start_game)
        draw_pop_button(quit_img, quit_size, quit_rect, 1.2, quit_game)
        draw_pop_button(settings_img, settings_size, settings_rect, 1.2, settings_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

main_menu()
