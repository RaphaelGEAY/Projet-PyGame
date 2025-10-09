from Vehicules.Vehicule import Vehicule

class VoitureDeBase(Vehicule):
    def __init__(self):
        super().__init__("VoitureDeBase.png", vitesseH=5, vitesseV=5, multiplicateur=1.0)
