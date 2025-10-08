from Obstacles.Obstacle import Obstacle

class VoitureOrange(Obstacle):
	def __init__(self, x, y):
		super().__init__(x, y, 50, 100, (255, 140, 0))
