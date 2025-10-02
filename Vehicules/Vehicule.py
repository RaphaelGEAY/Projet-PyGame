class Vehicule:
    def __init__(self, vitesseH, vitesseV, multiplicateur):
        self.vitesseH = vitesseH
        self.vitesseV = vitesseV
        self.multiplicateur = multiplicateur

    def deplacement_h(self):
        raise NotImplementedError("Cette méthode doit être redéfinie dans la classe fille.")

    def boost(self):
        raise NotImplementedError("Cette méthode doit être redéfinie dans la classe fille.")
