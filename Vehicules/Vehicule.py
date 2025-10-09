class Vehicule:
	def __init__(self, vitesseH, vitesseV, multiplicateur):
		self.vitesseH = vitesseH
		self.vitesseV = vitesseV
		self.multiplicateur = multiplicateur

	def deplacement_h(self):
		return int(self.vitesseH * self.multiplicateur)
	
	def boost(self):
		return int(self.vitesseV * self.multiplicateur)
