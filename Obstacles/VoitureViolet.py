from Obstacles.Obstacle import Obstacle

class VoitureViolet(Obstacle):
    def __init__(self, x, y):
        super().__init__("VoitureViolet.png", x, y, 40, 80)
