from Vehicules.Vehicule import Vehicule

class VoitureDeCourse(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=10, vitesseV=10, multiplicateur=1.5)
