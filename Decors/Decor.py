import pygame

class Decor:
	def __init__(self, color):
		self.color = color

	def draw(self, screen):
		screen.fill(self.color)
