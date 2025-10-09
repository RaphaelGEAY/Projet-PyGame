from Obstacles.Obstacle import Obstacle

class VoitureNoire(Obstacle):
    def __init__(self, x, y):
        super().__init__("VoitureNoire.png", x, y, 40, 80)
