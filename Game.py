


import pygame
import sys
import random
from Vehicules.Fourgon import Fourgon
from Vehicules.VoitureDeBase import VoitureDeBase
from Vehicules.VoitureDeCourse import VoitureDeCourse
from Vehicules.Moto import Moto
from Vehicules.Velo import Velo


# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu d'esquive d'obstacles 2D")

# Couleurs
GREEN = (34, 139, 34)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
OBSTACLE_COLORS = [(0,0,0), (0,120,215), (255,140,0), (128,0,128)]



# Liste des véhicules disponibles
vehicules = [VoitureDeBase(), VoitureDeCourse(), Fourgon(), Moto(), Velo()]
vehicule_names = ["Voiture de base", "Voiture de course", "Fourgon", "Moto", "Vélo"]
vehicule_index = 0
vehicule = vehicules[vehicule_index]


car_width, car_height = 40, 60
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 30
car_vel = 0
car_friction = 0.15

# Boost
boost_obstacle_speed = 4

# Route
road_width = 300
road_x = WIDTH // 2 - road_width // 2


# Obstacles
obstacles = []
obstacle_timer = 0
obstacle_interval = 40  # frames
obstacle_base_speed = 7



clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
score_font = pygame.font.SysFont(None, 36)
game_over = False
score = 0

# Animation des lignes blanches
line_offset = 0
line_speed = 8
# Vitesse verticale globale (utilisée partout)
global_vertical_speed = obstacle_base_speed

# Décalage vertical de la voiture lors du boost
boost_offset = 0

def spawn_obstacle():
    obs_width = random.randint(30, 70)
    obs_height = random.randint(30, 60)
    obs_x = random.randint(road_x, road_x + road_width - obs_width)
    obs_y = -obs_height
    color = random.choice(OBSTACLE_COLORS)
    # 30% des obstacles zigzaguent
    zigzag = random.random() < 0.3
    zigzag_speed = random.choice([-2, 2]) if zigzag else 0
    obstacles.append({
        "rect": pygame.Rect(obs_x, obs_y, obs_width, obs_height),
        "color": color,
        "zigzag": zigzag,
        "zigzag_speed": zigzag_speed
    })

def game():
	while True:

		# Gestion des événements (une seule fois par frame)
		events = pygame.event.get()
		restart_rect = None
		keys = pygame.key.get_pressed()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if not game_over and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_TAB:
					vehicule_index = (vehicule_index + 1) % len(vehicules)
					vehicule = vehicules[vehicule_index]
					car_x = WIDTH // 2 - car_width // 2
					car_vel = 0

		# Effet boost : déplacement vers l'avant
		max_boost_offset = 60
		boost_up_speed = 4
		boost_down_speed = 3
		if not game_over:
			if keys[pygame.K_SPACE]:
				if boost_offset < max_boost_offset:
					boost_offset += boost_up_speed
			else:
				if boost_offset > 0:
					boost_offset -= boost_down_speed

		if not game_over:
			min_road_width = 120
			road_width = max(min_road_width, 300 - score // 100)
			road_x = WIDTH // 2 - road_width // 2

			if keys[pygame.K_LEFT]:
				car_x -= vehicule.deplacement_h()
			if keys[pygame.K_RIGHT]:
				car_x += vehicule.deplacement_h()

			if car_x < road_x:
				car_x = road_x
				car_vel = 0
			if car_x + car_width > road_x + road_width:
				car_x = road_x + road_width - car_width
				car_vel = 0

			obstacle_timer += 1
			if obstacle_timer >= obstacle_interval:
				spawn_obstacle()
				obstacle_timer = 0

			if keys[pygame.K_SPACE]:
				global_vertical_speed = obstacle_base_speed + score // 120 + vehicule.boost()
			else:
				global_vertical_speed = obstacle_base_speed + score // 120

			for obs in obstacles:
				obs["rect"].y += global_vertical_speed
				if obs["zigzag"]:
					obs["rect"].x += obs["zigzag_speed"]
					if obs["rect"].x < road_x:
						obs["rect"].x = road_x
						obs["zigzag_speed"] *= -1
					if obs["rect"].x + obs["rect"].width > road_x + road_width:
						obs["rect"].x = road_x + road_width - obs["rect"].width
						obs["zigzag_speed"] *= -1

			car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
			for obs in obstacles:
				if car_rect.colliderect(obs["rect"]):
					game_over = True

			obstacles = [obs for obs in obstacles if obs["rect"].y < HEIGHT]

			score += 1

		screen.fill(GREEN)
		pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, HEIGHT))

		side_line_width = 8
		pygame.draw.rect(screen, WHITE, (road_x + 18, 0, side_line_width, HEIGHT))
		pygame.draw.rect(screen, WHITE, (road_x + road_width - 18 - side_line_width, 0, side_line_width, HEIGHT))

		if not game_over:
			line_offset = (line_offset + global_vertical_speed) % 40
		for i in range(-40, HEIGHT, 40):
			pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, i + line_offset, 10, 30))

		for obs in obstacles:
			pygame.draw.rect(screen, obs["color"], obs["rect"])

		car_y_boosted = car_y - boost_offset
		pygame.draw.rect(screen, RED, (car_x, car_y_boosted, car_width, car_height))

		change_rect = pygame.Rect(WIDTH - 180, 20, 160, 40)
		pygame.draw.rect(screen, (0, 120, 215), change_rect)
		change_font = pygame.font.SysFont(None, 28)
		change_text = change_font.render("Changer véhicule", True, WHITE)
		screen.blit(change_text, change_text.get_rect(center=change_rect.center))

		name_font = pygame.font.SysFont(None, 28)
		name_text = name_font.render(f"Véhicule : {vehicule_names[vehicule_index]}", True, (0, 0, 0))
		screen.blit(name_text, (20, 60))

		score_text = score_font.render(f"Score : {score}", True, (0, 0, 0))
		screen.blit(score_text, (20, 20))

		if game_over:
			text = font.render("Game Over!", True, (255, 0, 0))
			text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
			screen.blit(text, text_rect)

			restart_font = pygame.font.SysFont(None, 40)
			restart_text = restart_font.render("Restart", True, WHITE)
			restart_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 10, 140, 50)
			pygame.draw.rect(screen, (0, 120, 215), restart_rect)
			screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

		pygame.display.flip()
		clock.tick(60)

		if game_over and restart_rect is not None:
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if restart_rect.collidepoint(event.pos):
						car_x = WIDTH // 2 - car_width // 2
						car_vel = 0
						obstacles = []
						obstacle_timer = 0
						score = 0
						game_over = False

		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if change_rect.collidepoint(event.pos):
					vehicule_index = (vehicule_index + 1) % len(vehicules)
					vehicule = vehicules[vehicule_index]
					car_x = WIDTH // 2 - car_width // 2
					car_vel = 0


# Initialisation de Pygame
pygame.init()

WIDTH, HEIGHT = 1200, 630
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu Example")

background = pygame.image.load("Menus/Fond_menu.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

shop_background = pygame.image.load("Menus/Shop_menu.png")  
shop_background = pygame.transform.scale(shop_background, (WIDTH, HEIGHT))

title_image = pygame.image.load("Menus/SPEED_RUN.png")
title_rect = title_image.get_rect(center=(WIDTH / 2, 70))

start_img = pygame.image.load("Menus/START.png").convert_alpha()
shop_img = pygame.image.load("Menus/SHOP.png").convert_alpha()
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
            pygame.time.wait(150)
            action()
    else:
        screen.blit(image, rect)

def shop_menu():
    while True:
        screen.blit(shop_background, (0, 0))  

        shop_text = font.render( None, None, (255, 255, 255))
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
                pygame.quit()
                sys.exit()

        pygame.display.update()


main_menu()
