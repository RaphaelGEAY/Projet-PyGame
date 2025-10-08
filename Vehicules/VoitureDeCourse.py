from Vehicules.Vehicule import Vehicule

class VoitureDeCourse(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=7, vitesseV=7, multiplicateur=1.5)

	def deplacement_h(self):
		return self.vitesseH * self.multiplicateur

	def boost(self):
		return self.vitesseV * self.multiplicateur
