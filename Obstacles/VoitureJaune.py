from Obstacles.Obstacle import Obstacle

class VoitureJaune(Obstacle):
    def __init__(self, x, y):
        super().__init__("VoitureJaune.png", x, y, 40, 80)
