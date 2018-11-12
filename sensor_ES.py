import datetime as Date
from threading import Timer

currDate = Date.datetime.now()
numSpaces = 130
numCars = 0
spaces = []

# [Prob. Entrar, Prob. Sair]
probs = [
			[0, 0.05], 		# 00:00 -> 01:00
			[0, 0.05], 		# 01:00 -> 02:00
			[0, 0], 		# 02:00 -> 03:00
			[0, 0], 		# 03:00 -> 04:00
			[0, 0], 		# 04:00 -> 05:00
			[0.05, 0], 		# 05:00 -> 06:00
			[0.15, 0.05], 	# 06:00 -> 07:00
			[1.25, 0.05], 	# 07:00 -> 08:00
			[2, 0.05], 		# 08:00 -> 09:00
			[1.25, 0.05], 	# 09:00 -> 10:00
			[0.3, 0.05], 	# 10:00 -> 11:00
			[0.3, 0.05], 	# 11:00 -> 12:00
			[0.25, 0.6], 	# 12:00 -> 13:00
			[1.5, 0.25], 	# 13:00 -> 14:00
			[1, 0.4], 		# 14:00 -> 15:00
			[0.4, 0.5], 	# 15:00 -> 16:00
			[0.25, 0.5], 	# 16:00 -> 17:00
			[0.15, 0.5], 	# 17:00 -> 18:00
			[0.1, 0.25], 	# 18:00 -> 19:00
			[0.1, 0.25], 	# 19:00 -> 20:00
			[0.05, 1.25], 	# 20:00 -> 21:00
			[0.05, 1.25], 	# 21:00 -> 22:00
			[0, 1.5], 		# 22:00 -> 23:00
			[0, 4.5]] 		# 23:00 -> 24:00


def main():
	global spaces
	global currDate

	for i in range(24):
		spaces.append(0)

	currDate = Date.datetime.now()

	if currDate.second <= 56:  # Se esta prestes a mudar de minuto espera para o proximo minuto
		aux = 60
	else:
		aux = 120

	set_timeout(aux - 1 - currDate.second + 0.0, start)


def set_timeout(timeout, func):
	t = Timer(timeout, func)
	t.start()


def start():
	global currDate
	while currDate.second != 0:  # Poll se ja mudou de minuto (mais preciso que criar o timer abaixo quando muda o minuto)
		currDate = Date.datetime.now()
	simulate()


def simulate():
	import random
	import math

	global numCars
	global currDate
	global spaces

	if numCars < numSpaces and random.uniform(0, 100) < probs[currDate.hour][0]:
		numCars += 1
		print("Entrou um carro as ", currDate.hour, "h", currDate.minute, "m\n")

	remove = math.floor(random.randint(0, 5))

	if numCars >= remove and random.uniform(0, 100) < probs[currDate.hour][1]:
		numCars -= remove
		print("Saiu ", remove, " carro(s) as ", currDate.hour, "h", currDate.minute, "m\n")

	if currDate.hour == 0:
		spaces = []
		numCars = 0
	else:
		spaces[currDate.hour] = numCars

	currDate = Date.datetime.now()
	set_timeout(1, simulate)


if __name__ == "__main__":
	main()
