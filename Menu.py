import pygame, sys
import Game

pygame.init()

WIDTH, HEIGHT = 1200, 630
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speed Run Menu")

background = pygame.image.load("Menus/Fond_menu.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
shop_background = pygame.image.load("Menus/Shop_menu.png")
shop_background = pygame.transform.scale(shop_background, (WIDTH, HEIGHT))

title_image = pygame.image.load("Menus/SPEED_RUN.png")
title_rect = title_image.get_rect(center=(WIDTH / 2, 70))

start_img = pygame.image.load("Menus/START.png").convert_alpha()
shop_img = pygame.image.load("Menus/Shop.png").convert_alpha()
quit_img = pygame.image.load("Menus/QUIT.png").convert_alpha()
settings_img = pygame.image.load("Menus/Settings.png").convert_alpha()

start_size = (260, 190)
quit_size = (260, 200)
shop_size = (270, 250)
settings_size = (180, 180)

start_img = pygame.transform.scale(start_img, start_size)
quit_img = pygame.transform.scale(quit_img, quit_size)
shop_img = pygame.transform.scale(shop_img, shop_size)
settings_img = pygame.transform.scale(settings_img, settings_size)

start_rect = start_img.get_rect(center=(WIDTH // 2, 250))
shop_rect = shop_img.get_rect(center=(WIDTH // 2, 405))
quit_rect = quit_img.get_rect(center=(WIDTH // 2, 560))
settings_rect = settings_img.get_rect(center=(WIDTH - 120, 500))

font = pygame.font.Font(None, 100)

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

def quit_game():
	pygame.quit()
	sys.exit()

def shop_menu():
	while True:
		screen.blit(shop_background, (0, 0))
		back_font = pygame.font.Font(None, 60)
		back_text = back_font.render("Back", True, (255, 255, 255))
		back_rect = back_text.get_rect(center=(100, 50))
		screen.blit(back_text, back_rect)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if back_rect.collidepoint(event.pos):
					return
		pygame.display.update()

def settings_game():
	print("Settings menu (à compléter)")

def start_game():
	Game.run_game()

def main_menu():
	while True:
		screen.blit(background, (0, 0))
		screen.blit(title_image, title_rect)
		draw_pop_button(start_img, start_size, start_rect, 1.2, start_game)
		draw_pop_button(shop_img, shop_size, shop_rect, 1.2, shop_menu)
		draw_pop_button(quit_img, quit_size, quit_rect, 1.2, quit_game)
		draw_pop_button(settings_img, settings_size, settings_rect, 1.2, settings_game)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit_game()

		pygame.display.update()

main_menu()
