from Obstacles.Obstacle import Obstacle

class VoitureViolet(Obstacle):
	def __init__(self, x, y):
		super().__init__(x, y, 50, 100, (200, 0, 200))
