from Vehicules.Vehicule import Vehicule

class Velo(Vehicule):
    def __init__(self):
        super().__init__("Velo.png", vitesseH=3, vitesseV=1, multiplicateur=1.0)
