from Vehicules.Vehicule import Vehicule

class Velo(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=5, vitesseV=1, multiplicateur=0.8)

	def deplacement_h(self):
		return self.vitesseH * self.multiplicateur

	def boost(self):
		return self.vitesseV * self.multiplicateur
