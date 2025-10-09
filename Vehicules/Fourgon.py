from Vehicules.Vehicule import Vehicule

class Fourgon(Vehicule):
    def __init__(self):
        super().__init__("Fourgon.png", vitesseH=3, vitesseV=3, multiplicateur=0.7)
