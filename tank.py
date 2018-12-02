import pygame

TANKS = {}

class Tank:

	def __init__(self, ID, speed, health, fuel):
		self.image = pygame.image.load('assets/tanks/tank_{}.png'.format(ID))#.convert()
		self.speed = speed
		self.health = health
		self.fuel = fuel

		global TANKS
		TANKS[ID] = self

	def launch(self):
		pass

class TankDefault(Tank):

	def __init__(self):
		Tank.__init__(self, 1, 5, 100, 100)

	def launch(self):
		pass