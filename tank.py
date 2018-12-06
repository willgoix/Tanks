import pygame, bullet

TANKS = {}


class Tank:

	def __init__(self, ID, speed, health, fuel):
		self.image = pygame.transform.scale(pygame.image.load('assets/tanks/tank_{}.png'.format(ID)), (40, 40))
		self.speed = speed
		self.health = health
		self.fuel = fuel

		global TANKS
		TANKS[ID] = self

	def launch(self, pos, shooter, target=None):
		pass


class TankDefault(Tank):

	def __init__(self):
		Tank.__init__(self, 1, 4, 100, 100)

	def launch(self, pos, shooter, target=None):
		bullet.Bullet.from_local(pos, 10, shooter, target)