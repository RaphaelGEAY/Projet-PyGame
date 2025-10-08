from Obstacles.Obstacle import Obstacle

class Rampe(Obstacle):
	def __init__(self, x, y):
		super().__init__(x, y, 150, 150, (180, 180, 180))
