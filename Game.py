import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 630
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu Example")

background = pygame.image.load("55492cea-b28c-4260-85cb-6b1210f78496.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

title_image = pygame.image.load("generated_text (1).png")
title_rect = title_image.get_rect(center=(WIDTH / 2, 70))

shop_background = pygame.image.load("SHOPPY.png")  
shop_background = pygame.transform.scale(shop_background, (WIDTH, HEIGHT))

start_img = pygame.image.load("START.png").convert_alpha()
quit_img = pygame.image.load("QUIT.png").convert_alpha()
shop_img = pygame.image.load("SHO.png").convert_alpha()
settings_img = pygame.image.load("SETTINGS.png").convert_alpha()

start_size = (260, 140)
quit_size = (230, 120)
shop_size = (265, 130)
settings_size = (180, 180)

start_img = pygame.transform.scale(start_img, start_size)
quit_img = pygame.transform.scale(quit_img, quit_size)
shop_img = pygame.transform.scale(shop_img, shop_size)
settings_img = pygame.transform.scale(settings_img, settings_size)

start_rect = start_img.get_rect(center=(WIDTH // 2.01, 250))
quit_rect = quit_img.get_rect(center=(WIDTH // 2, 560))
shop_rect = shop_img.get_rect(center=(WIDTH // 2, 410))
settings_rect = settings_img.get_rect(center=(WIDTH - 120, 500))

font = pygame.font.Font(None, 100)

sound_on_img = pygame.image.load("sound_on_img.png").convert_alpha()
sound_off_img = pygame.image.load("sound_off_img.png").convert_alpha()

sound_icon_size = (80, 80)
sound_on_img = pygame.transform.scale(sound_on_img, sound_icon_size)
sound_off_img = pygame.transform.scale(sound_off_img, sound_icon_size)

sound_rect = sound_on_img.get_rect(center=(WIDTH / 2 + 150, 250))

sound_on = True

def shop_menu():
    while True:
        screen.blit(shop_background, (0, 0))

        shop_text = font.render("SHOP", True, (255, 255, 255))
        shop_rect_text = shop_text.get_rect(center=(WIDTH / 2, 100))
        screen.blit(shop_text, shop_rect_text)

        back_font = pygame.font.Font(None, 60)
        back_text = back_font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(100, 50))
        screen.blit(back_text, back_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    main_menu()

        pygame.display.update()

def settings_menu():
    global sound_on

    while True:
        screen.fill((30, 60, 90))

        settings_text = font.render("SETTINGS", True, (255, 255, 255))
        settings_rect_text = settings_text.get_rect(center=(WIDTH / 2, 100))
        screen.blit(settings_text, settings_rect_text)

        option_font = pygame.font.Font(None, 50)
        volume_text = option_font.render("Volume:", True, (200, 200, 200))
        screen.blit(volume_text, (WIDTH / 2 - 150, 230))

        if sound_on:
            screen.blit(sound_on_img, sound_rect)
        else:
            screen.blit(sound_off_img, sound_rect)

        back_font = pygame.font.Font(None, 60)
        back_text = back_font.render("Back", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(100, 50))
        screen.blit(back_text, back_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    main_menu()

                if sound_rect.collidepoint(event.pos):
                    sound_on = not sound_on
                    print("Sound On" if sound_on else "Sound Off")

        pygame.display.update()

def draw_pop_button(image, base_size, rect, scale_factor=1.2, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        new_size = (int(base_size[0] * scale_factor), int(base_size[1] * scale_factor))
        scaled_img = pygame.transform.scale(image, new_size)
        new_rect = scaled_img.get_rect(center=rect.center)
        screen.blit(scaled_img, new_rect)

        if click[0] == 1 and action is not None:
            pygame.time.wait(150)
            action()
    else:
        screen.blit(image, rect)


def start_game():
    print("Game Started!")


def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    while True:
        screen.blit(background, (0, 0))
        screen.blit(title_image, title_rect)

        draw_pop_button(start_img, start_size, start_rect, 1.2, start_game)
        draw_pop_button(shop_img, shop_size, shop_rect, 1.2, shop_menu)
        draw_pop_button(quit_img, quit_size, quit_rect, 1.2, quit_game)
        draw_pop_button(settings_img, settings_size, settings_rect, 1.2, settings_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main_menu()
