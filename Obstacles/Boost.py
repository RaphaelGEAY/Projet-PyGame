from Obstacles.Obstacle import Obstacle

class Boost(Obstacle):
    def __init__(self, x, y):
        super().__init__("Boost.png", x, y, 150, 150)
