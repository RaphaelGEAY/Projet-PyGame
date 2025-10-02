from Vehicules.Vehicule import Vehicule

class Velo(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=3, vitesseV=2, multiplicateur=0.9)

	def deplacement_h(self):
		return self.vitesseH * self.multiplicateur

	def boost(self):
		return self.vitesseV * self.multiplicateur
