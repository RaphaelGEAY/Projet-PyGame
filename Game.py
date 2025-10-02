

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
car_vel = 0
car_acc = 0.7
car_friction = 0.15
car_max_speed = 10
# Boost
boost_obstacle_speed = 4  # vitesse supplémentaire plus raisonnable

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
            if event.key == pygame.K_LEFT:
                car_vel = -car_max_speed
            if event.key == pygame.K_RIGHT:
                car_vel = car_max_speed

    if not game_over:
        # Réduction progressive de la largeur de la route
        min_road_width = 120
        road_width = max(min_road_width, 300 - score // 100)
        road_x = WIDTH // 2 - road_width // 2

        # Décélération naturelle
        if car_vel > 0:
            car_vel -= car_friction
            if car_vel < 0:
                car_vel = 0
        elif car_vel < 0:
            car_vel += car_friction
            if car_vel > 0:
                car_vel = 0
        car_x += car_vel

        # Empêcher la voiture de sortir de la route
        if car_x < road_x:
            car_x = road_x
            car_vel = 0
        if car_x + car_width > road_x + road_width:
            car_x = road_x + road_width - car_width
            car_vel = 0

        # Génération d'obstacles
        obstacle_timer += 1
        if obstacle_timer >= obstacle_interval:
            spawn_obstacle()
            obstacle_timer = 0

        # Boost sur la vitesse des obstacles (tant que ESPACE est maintenu)
        if keys[pygame.K_SPACE]:
            obstacle_speed = obstacle_base_speed + score // 120 + boost_obstacle_speed
        else:
            obstacle_speed = obstacle_base_speed + score // 120

        for obs in obstacles:
            obs["rect"].y += obstacle_speed
            # Zigzag horizontal
            if obs["zigzag"]:
                obs["rect"].x += obs["zigzag_speed"]
                # Rebondir sur les bords de la route
                if obs["rect"].x < road_x:
                    obs["rect"].x = road_x
                    obs["zigzag_speed"] *= -1
                if obs["rect"].x + obs["rect"].width > road_x + road_width:
                    obs["rect"].x = road_x + road_width - obs["rect"].width
                    obs["zigzag_speed"] *= -1

        # Collision
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        for obs in obstacles:
            if car_rect.colliderect(obs["rect"]):
                game_over = True

        # Retirer les obstacles hors écran
        obstacles = [obs for obs in obstacles if obs["rect"].y < HEIGHT]

        # Score
        score += 1

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

    # Affichage du score
    score_text = score_font.render(f"Score : {score}", True, (0,0,0))
    screen.blit(score_text, (20, 20))

    # Affichage Game Over et bouton Restart
    if game_over:
        text = font.render("Game Over!", True, (255,0,0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        screen.blit(text, text_rect)

        restart_font = pygame.font.SysFont(None, 40)
        restart_text = restart_font.render("Restart", True, WHITE)
        restart_rect = pygame.Rect(WIDTH//2 - 70, HEIGHT//2 + 10, 140, 50)
        pygame.draw.rect(screen, (0,120,215), restart_rect)
        screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

    pygame.display.flip()
    clock.tick(60)

    # Gestion du clic sur le bouton Restart
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
