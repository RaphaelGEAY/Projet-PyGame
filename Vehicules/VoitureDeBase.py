from Vehicules.Vehicule import Vehicule

class VoitureDeBase(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=5, vitesseV=5, multiplicateur=1.0)

	def deplacement_h(self):
		return self.vitesseH * self.multiplicateur

	def boost(self):
		return self.vitesseV * self.multiplicateur
