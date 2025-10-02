

import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

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

# Voiture
car_width, car_height = 40, 60
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 30
car_speed = 7

# Route
road_width = 300
road_x = WIDTH // 2 - road_width // 2

# Obstacles
obstacles = []
obstacle_timer = 0
obstacle_interval = 40  # frames

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
game_over = False

def spawn_obstacle():
    obs_width = random.randint(30, 70)
    obs_height = random.randint(30, 60)
    obs_x = random.randint(road_x, road_x + road_width - obs_width)
    obs_y = -obs_height
    color = random.choice(OBSTACLE_COLORS)
    obstacles.append({"rect": pygame.Rect(obs_x, obs_y, obs_width, obs_height), "color": color})

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Contrôles clavier (gauche/droite uniquement)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car_x -= car_speed
        if keys[pygame.K_RIGHT]:
            car_x += car_speed

        # Empêcher la voiture de sortir de la route
        if car_x < road_x:
            car_x = road_x
        if car_x + car_width > road_x + road_width:
            car_x = road_x + road_width - car_width

        # Génération d'obstacles
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            spawn_obstacle()
            obstacle_timer = 0

        # Mouvement des obstacles
        for obs in obstacles:
            obs["rect"].y += 7

        # Collision
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        for obs in obstacles:
            if car_rect.colliderect(obs["rect"]):
                game_over = True

        # Retirer les obstacles hors écran
        obstacles = [obs for obs in obstacles if obs["rect"].y < HEIGHT]

    # Dessin de la carte
    screen.fill(GREEN)  # Herbe
    pygame.draw.rect(screen, GRAY, (road_x, 0, road_width, HEIGHT))  # Route
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i, 10, 30))

    # Dessin des obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, obs["color"], obs["rect"])

    # Dessin de la voiture
    pygame.draw.rect(screen, RED, (car_x, car_y, car_width, car_height))

    if game_over:
        text = font.render("Game Over!", True, (255,0,0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)
