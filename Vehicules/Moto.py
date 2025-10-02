from Vehicules.Vehicule import Vehicule

class Moto(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=8, vitesseV=6, multiplicateur=1.2)

	def deplacement_h(self):
		return self.vitesseH * self.multiplicateur

	def boost(self):
		return self.vitesseV * self.multiplicateur
