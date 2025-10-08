from Obstacles.Obstacle import Obstacle

class BarrierePolice(Obstacle):
	def __init__(self, x, y):
		super().__init__(x, y, 450, 150, (180, 180, 180))
