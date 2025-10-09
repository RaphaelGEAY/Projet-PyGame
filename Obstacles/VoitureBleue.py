from Obstacles.Obstacle import Obstacle

class VoitureBleue(Obstacle):
    def __init__(self, x, y):
        super().__init__("VoitureBleue.png", x, y, 40, 80)
