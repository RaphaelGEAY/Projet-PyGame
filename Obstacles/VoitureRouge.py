from Obstacles.Obstacle import Obstacle

class VoitureRouge(Obstacle):
	def __init__(self, x, y):
		super().__init__(x, y, 50, 80, (255, 0, 0))
