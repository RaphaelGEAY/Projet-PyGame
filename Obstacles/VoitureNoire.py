from Obstacles.Obstacle import Obstacle

class VoitureNoire(Obstacle):
	def __init__(self, x, y):
		super().__init__(x, y, 50, 80, (0, 0, 0))
