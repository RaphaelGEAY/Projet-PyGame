from Obstacles.Obstacle import Obstacle

class VoitureOrange(Obstacle):
    def __init__(self, x, y):
        super().__init__("VoitureOrange.png", x, y, 40, 80)
