import pygame, sys, random
from Vehicules.Fourgon import Fourgon
from Vehicules.VoitureDeBase import VoitureDeBase
from Vehicules.VoitureDeCourse import VoitureDeCourse
from Vehicules.Moto import Moto
from Vehicules.Velo import Velo

class Game:
	def __init__(self):
		pygame.init()
		self.WIDTH, self.HEIGHT = 800, 600
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("Jeu d'esquive d'obstacles 2D")

		self.GREEN = (34, 139, 34)
		self.GRAY = (120, 120, 120)
		self.WHITE = (255, 255, 255)
		self.RED = (200, 0, 0)
		self.OBSTACLE_COLORS = [(0,0,0), (0,120,215), (255,140,0), (128,0,128)]

		self.vehicules = [VoitureDeBase(), VoitureDeCourse(), Fourgon(), Moto(), Velo()]
		self.vehicule_names = ["Voiture de base", "Voiture de course", "Fourgon", "Moto", "Vélo"]
		self.vehicule_index = 0
		self.vehicule = self.vehicules[self.vehicule_index]

		self.car_width, self.car_height = 40, 60
		self.car_x = self.WIDTH // 2 - self.car_width // 2
		self.car_y = self.HEIGHT - self.car_height - 30
		self.car_vel = 0
		self.car_friction = 0.15
		self.boost_obstacle_speed = 4
		self.road_width = 300
		self.road_x = self.WIDTH // 2 - self.road_width // 2

		self.obstacles = []
		self.obstacle_timer = 0
		self.obstacle_interval = 40
		self.obstacle_base_speed = 7

		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont(None, 48)
		self.score_font = pygame.font.SysFont(None, 36)
		self.game_over = False
		self.score = 0
		self.line_offset = 0
		self.global_vertical_speed = self.obstacle_base_speed
		self.boost_offset = 0

	def spawn_obstacle(self):
		obs_width = random.randint(30, 70)
		obs_height = random.randint(30, 60)
		obs_x = random.randint(self.road_x, self.road_x + self.road_width - obs_width)
		obs_y = -obs_height
		color = random.choice(self.OBSTACLE_COLORS)
		zigzag = random.random() < 0.3
		zigzag_speed = random.choice([-2, 2]) if zigzag else 0
		self.obstacles.append({
			"rect": pygame.Rect(obs_x, obs_y, obs_width, obs_height),
			"color": color,
			"zigzag": zigzag,
			"zigzag_speed": zigzag_speed
		})

	def restart(self):
		self.car_x = self.WIDTH // 2 - self.car_width // 2
		self.car_vel = 0
		self.obstacles = []
		self.obstacle_timer = 0
		self.score = 0
		self.game_over = False

	def run(self):
		while True:
			events = pygame.event.get()
			restart_rect = None
			keys = pygame.key.get_pressed()

			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if not self.game_over and event.type == pygame.KEYDOWN:
					if event.key == pygame.K_TAB:
						self.vehicule_index = (self.vehicule_index + 1) % len(self.vehicules)
						self.vehicule = self.vehicules[self.vehicule_index]
						self.car_x = self.WIDTH // 2 - self.car_width // 2
						self.car_vel = 0

			max_boost_offset = 60
			boost_up_speed = 4
			boost_down_speed = 3
			if not self.game_over:
				if keys[pygame.K_SPACE]:
					if self.boost_offset < max_boost_offset:
						self.boost_offset += boost_up_speed
				else:
					if self.boost_offset > 0:
						self.boost_offset -= boost_down_speed

			if not self.game_over:
				min_road_width = 120
				self.road_width = max(min_road_width, 300 - self.score // 100)
				self.road_x = self.WIDTH // 2 - self.road_width // 2

				if keys[pygame.K_LEFT]:
					self.car_x -= self.vehicule.deplacement_h()
				if keys[pygame.K_RIGHT]:
					self.car_x += self.vehicule.deplacement_h()

				if self.car_x < self.road_x:
					self.car_x = self.road_x
				if self.car_x + self.car_width > self.road_x + self.road_width:
					self.car_x = self.road_x + self.road_width - self.car_width

				self.obstacle_timer += 1
				if self.obstacle_timer >= self.obstacle_interval:
					self.spawn_obstacle()
					self.obstacle_timer = 0

				if keys[pygame.K_SPACE]:
					self.global_vertical_speed = self.obstacle_base_speed + self.score // 120 + self.vehicule.boost()
				else:
					self.global_vertical_speed = self.obstacle_base_speed + self.score // 120

				for obs in self.obstacles:
					obs["rect"].y += self.global_vertical_speed
					if obs["zigzag"]:
						obs["rect"].x += obs["zigzag_speed"]
						if obs["rect"].x < self.road_x:
							obs["rect"].x = self.road_x
							obs["zigzag_speed"] *= -1
						if obs["rect"].x + obs["rect"].width > self.road_x + self.road_width:
							obs["rect"].x = self.road_x + self.road_width - obs["rect"].width
							obs["zigzag_speed"] *= -1

				car_rect = pygame.Rect(self.car_x, self.car_y, self.car_width, self.car_height)
				for obs in self.obstacles:
					if car_rect.colliderect(obs["rect"]):
						self.game_over = True

				self.obstacles = [obs for obs in self.obstacles if obs["rect"].y < self.HEIGHT]
				self.score += 1

			self.screen.fill(self.GREEN)
			pygame.draw.rect(self.screen, self.GRAY, (self.road_x, 0, self.road_width, self.HEIGHT))

			side_line_width = 8
			pygame.draw.rect(self.screen, self.WHITE, (self.road_x + 18, 0, side_line_width, self.HEIGHT))
			pygame.draw.rect(self.screen, self.WHITE, (self.road_x + self.road_width - 18 - side_line_width, 0, side_line_width, self.HEIGHT))

			if not self.game_over:
				self.line_offset = (self.line_offset + self.global_vertical_speed) % 40
			for i in range(-40, self.HEIGHT, 40):
				pygame.draw.rect(self.screen, self.WHITE, (self.WIDTH // 2 - 5, i + self.line_offset, 10, 30))

			for obs in self.obstacles:
				pygame.draw.rect(self.screen, obs["color"], obs["rect"])

			car_y_boosted = self.car_y - self.boost_offset
			pygame.draw.rect(self.screen, self.RED, (self.car_x, car_y_boosted, self.car_width, self.car_height))

			change_rect = pygame.Rect(self.WIDTH - 180, 20, 160, 40)
			pygame.draw.rect(self.screen, (0, 120, 215), change_rect)
			change_font = pygame.font.SysFont(None, 28)
			change_text = change_font.render("Changer véhicule", True, self.WHITE)
			self.screen.blit(change_text, change_text.get_rect(center=change_rect.center))

			name_font = pygame.font.SysFont(None, 28)
			name_text = name_font.render(f"Véhicule : {self.vehicule_names[self.vehicule_index]}", True, (0, 0, 0))
			self.screen.blit(name_text, (20, 60))

			score_text = self.score_font.render(f"Score : {self.score}", True, (0, 0, 0))
			self.screen.blit(score_text, (20, 20))

			if self.game_over:
				text = self.font.render("Game Over!", True, (255, 0, 0))
				text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 40))
				self.screen.blit(text, text_rect)
				restart_font = pygame.font.SysFont(None, 40)
				restart_text = restart_font.render("Restart", True, self.WHITE)
				restart_rect = pygame.Rect(self.WIDTH // 2 - 70, self.HEIGHT // 2 + 10, 140, 50)
				pygame.draw.rect(self.screen, (0, 120, 215), restart_rect)
				self.screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

			pygame.display.flip()
			self.clock.tick(60)

			if self.game_over and restart_rect is not None:
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN and restart_rect.collidepoint(event.pos):
						self.restart()

			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN and change_rect.collidepoint(event.pos):
					self.vehicule_index = (self.vehicule_index + 1) % len(self.vehicules)
					self.vehicule = self.vehicules[self.vehicule_index]
					self.car_x = self.WIDTH // 2 - self.car_width // 2
					self.car_vel = 0

def run_game():
	game = Game()
	game.run()
