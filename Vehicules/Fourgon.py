from Vehicules.Vehicule import Vehicule

class Fourgon(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=3, vitesseV=1, multiplicateur=1.0)

	def deplacement_h(self):
		return self.vitesseH * self.multiplicateur

	def boost(self):
		return self.vitesseV * self.multiplicateur
