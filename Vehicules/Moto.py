from Vehicules.Vehicule import Vehicule

class Moto(Vehicule):
	def __init__(self):
		super().__init__(vitesseH=7, vitesseV=7, multiplicateur=1.2)
