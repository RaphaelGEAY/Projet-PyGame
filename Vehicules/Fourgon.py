from Vehicules.Vehicule import Vehicule

class Fourgon(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=4, vitesseV=3, multiplicateur=1.1)

	def deplacement_h(self):
		return self.vitesseH * self.multiplicateur

	def boost(self):
		return self.vitesseV * self.multiplicateur
