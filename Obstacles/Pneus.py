from Obstacles.Obstacle import Obstacle

class Pneus(Obstacle):
    def __init__(self, x, y):
        super().__init__("Pneus.png", x, y, 60, 60)
