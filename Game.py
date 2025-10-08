import pygame, sys, random
from Vehicules.Fourgon import Fourgon
from Vehicules.VoitureDeBase import VoitureDeBase
from Vehicules.VoitureDeCourse import VoitureDeCourse
from Vehicules.Moto import Moto
from Vehicules.Velo import Velo
from Obstacles.Obstacle import Obstacle
from Obstacles.VoitureBleue import VoitureRouge as VoitureBleue
from Obstacles.BarrierePolice import VoitureRouge as BarrierePolice

class Game:
	def __init__(self, go_to_menu_callback=None):
		pygame.init()
		self.WIDTH, self.HEIGHT = 1200, 700
		self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("SPEED RUN")

		self.GREEN = (34, 139, 34)
		self.GRAY = (120, 120, 120)
		self.WHITE = (255, 255, 255)
		self.RED = (200, 0, 0)
		self.BLUE = (0, 120, 215)
		self.DARK_GRAY = (60, 60, 60)

		self.vehicules = [VoitureDeBase(), VoitureDeCourse(), Fourgon(), Moto(), Velo()]
		self.vehicule_names = ["Voiture de base", "Voiture de course", "Fourgon", "Moto", "Vélo"]
		self.vehicule_index = 0
		self.vehicule = self.vehicules[self.vehicule_index]

		self.car_width, self.car_height = 40, 60
		self.car_x = self.WIDTH // 2 - self.car_width // 2
		self.car_y = self.HEIGHT - self.car_height - 30

		self.road_width = 300
		self.road_x = self.WIDTH // 2 - self.road_width // 2

		self.obstacles = []
		self.obstacle_timer = 0
		self.obstacle_interval = 40
		self.obstacle_base_speed = 7

		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont(None, 48)
		self.score_font = pygame.font.SysFont(None, 36)
		self.button_font = pygame.font.SysFont(None, 28)

		self.game_over = False
		self.score = 0
		self.line_offset = 0
		self.global_vertical_speed = self.obstacle_base_speed
		self.boost_offset = 0

		self.go_to_menu_callback = go_to_menu_callback

	def spawn_obstacle(self):
		type_obstacle = random.choice(["bleue", "barriere", "simple"])
		if type_obstacle == "bleue":
			x = random.randint(self.road_x, self.road_x + self.road_width - 50)
			y = -80
			obs = VoitureBleue(x, y)
		elif type_obstacle == "barriere":
			x = self.road_x + (self.road_width // 2) - 225
			y = -150
			obs = BarrierePolice(x, y)
		else:
			obs_width = random.randint(30, 70)
			obs_height = random.randint(30, 60)
			obs_x = random.randint(self.road_x, self.road_x + self.road_width - obs_width)
			obs_y = -obs_height
			color = random.choice([(0,0,0), (0,120,215), (255,140,0), (128,0,128)])
			obs = Obstacle(obs_x, obs_y, obs_width, obs_height, color)
		self.obstacles.append(obs)

	def restart(self):
		self.car_x = self.WIDTH // 2 - self.car_width // 2
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

			# Gestion du boost
			max_boost_offset = 60
			boost_up_speed = 4
			boost_down_speed = 3
			boosting = False
			if not self.game_over:
				if keys[pygame.K_SPACE]:
					if self.boost_offset < max_boost_offset:
						self.boost_offset += boost_up_speed
					boosting = True
				else:
					if self.boost_offset > 0:
						self.boost_offset -= boost_down_speed

			if not self.game_over:
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

				if boosting:
					self.global_vertical_speed = self.obstacle_base_speed + self.score // 120 + self.vehicule.boost()
				else:
					self.global_vertical_speed = self.obstacle_base_speed + self.score // 120

				for obs in self.obstacles:
					obs.update(self.global_vertical_speed)

				car_rect = pygame.Rect(self.car_x, self.car_y, self.car_width, self.car_height)
				for obs in self.obstacles:
					if isinstance(obs, BarrierePolice) and boosting:
						continue
					if car_rect.colliderect(obs.rect):
						self.game_over = True

				self.obstacles = [obs for obs in self.obstacles if obs.rect.y < self.HEIGHT]
				self.score += 1

			self.screen.fill(self.GREEN)
			pygame.draw.rect(self.screen, self.GRAY, (self.road_x, 0, self.road_width, self.HEIGHT))

			# Lignes blanches
			if not self.game_over:
				self.line_offset = (self.line_offset + self.global_vertical_speed) % 40
			for i in range(-40, self.HEIGHT, 40):
				pygame.draw.rect(self.screen, self.WHITE, (self.WIDTH // 2 - 5, i + self.line_offset, 10, 30))

			for obs in self.obstacles:
				obs.draw(self.screen)

			car_y_boosted = self.car_y - self.boost_offset
			pygame.draw.rect(self.screen, self.RED, (self.car_x, car_y_boosted, self.car_width, self.car_height))

			score_text = self.score_font.render(f"Score : {self.score}", True, (0, 0, 0))
			self.screen.blit(score_text, (20, 70))

			# Bouton Changer Véhicule
			change_rect = pygame.Rect(self.WIDTH - 200, 20, 180, 40)
			pygame.draw.rect(self.screen, self.BLUE, change_rect)
			change_text = self.button_font.render("Changer véhicule", True, self.WHITE)
			self.screen.blit(change_text, change_text.get_rect(center=change_rect.center))

			# Bouton Menu
			menu_rect = pygame.Rect(20, 20, 120, 40)
			pygame.draw.rect(self.screen, self.DARK_GRAY, menu_rect)
			menu_text = self.button_font.render("Menu", True, self.WHITE)
			self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))

			# Nom du véhicule
			name_text = self.button_font.render(f"Véhicule : {self.vehicule_names[self.vehicule_index]}", True, (0, 0, 0))
			self.screen.blit(name_text, (20, 130))

			if self.game_over:
				text = self.font.render("Game Over!", True, (255, 0, 0))
				text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 40))
				self.screen.blit(text, text_rect)
				restart_font = pygame.font.SysFont(None, 40)
				restart_text = restart_font.render("Restart", True, self.WHITE)
				restart_rect = pygame.Rect(self.WIDTH // 2 - 70, self.HEIGHT // 2 + 10, 140, 50)
				pygame.draw.rect(self.screen, self.BLUE, restart_rect)
				self.screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))

			pygame.display.flip()
			self.clock.tick(60)

			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if change_rect.collidepoint(event.pos):
						self.vehicule_index = (self.vehicule_index + 1) % len(self.vehicules)
						self.vehicule = self.vehicules[self.vehicule_index]
					elif menu_rect.collidepoint(event.pos):
						if self.go_to_menu_callback:
							self.go_to_menu_callback()
							return
						else:
							pygame.quit()
							sys.exit()
					elif self.game_over and restart_rect and restart_rect.collidepoint(event.pos):
						self.restart()

def run_game(go_to_menu_callback=None):
	game = Game(go_to_menu_callback)
	game.run()
