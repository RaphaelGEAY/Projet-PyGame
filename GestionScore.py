import os

class GestionScore:
	def __init__(self):
		self.fichier = "highscore.txt"
		self.meilleur_score = self.charger()

	def charger(self):
		try:
			if os.path.exists(self.fichier):
				with open(self.fichier, "r") as f:
					return int(f.read().strip())
		except:
			pass
		return 0

	def mettre_a_jour(self, score):
		self.meilleur_score = score
		try:
			with open(self.fichier, "w") as f:
				f.write(str(score))
		except:
			pass
