import pygame, my, explosion, math, sound, threading, lib.delayedfunc
from os import listdir

IMAGES = {}


def loadImages(directory):
	for filename in listdir(directory):
		image = pygame.image.load('{}/{}'.format(directory, filename))  # .convert()
		# image.set_colorkey((0, 0, 0, 0))
		IMAGES[filename.split(".")[0]] = image


class Bullet(pygame.sprite.Sprite):

	def __init__(self, pos, velocity, shooter):
		pygame.sprite.Sprite.__init__(self)
		my.ENGINE.game.entities.add(self)
		my.ENGINE.game.entities.setTarget(self)

		self.image = IMAGES['default_bullet']
		if velocity.x < 0:
			self.image = pygame.transform.flip(self.image, True, False)
		if velocity.y > -6:
			self.image = pygame.transform.flip(self.image, False, True)
		self.original = self.image.copy()

		self.pos = [pos[0], pos[1]]
		self.rect = self.image.get_rect(center=self.pos)
		self.startx = self.pos[0]

		self.velocity = velocity
		self.shooter = shooter
		self.firing = True
		self.DAMAGE = 10

		sound.play('launch')

	@staticmethod
	def from_local(pos, speed, shooter, target=None):
		x, y = pygame.mouse.get_pos() if target is None else target
		angle = 360 - math.atan2(y - pos[1], x - pos[0]) * 180 / math.pi

		velocityx = speed * math.cos(math.radians(360 - angle))
		velocityy = speed * math.sin(math.radians(360 - angle))
		velocity = pygame.Vector2((velocityx, velocityy))

		bullet = Bullet(pos, velocity, shooter)
		return bullet

	@staticmethod
	def from_network(pos, velocity, shooter):
		return Bullet(pos, velocity, shooter)

	def update(self):
		if self.hitDetect():
			# if self.gs.isServer:
			#	self.gs.remove_blocks(self.pos[0], self.pos[1])  # remove the blocks from the map
			#	data = pickle.dumps(elf.pos)  # serialize the data (might be overkill here but we wanted to be consistent)
			#	self.gs.terrainConnection.transport.write(data)

			explosion.Explosion(self.pos)
			my.ENGINE.game.entities.remove(self)

			lib.delayedfunc.DelayedFunc(lambda: my.ENGINE.game.turncontroller.next(), 2)
		else:
			acceleration = my.GRAVITY + my.ENGINE.game.wind.wind #TODO: Vento
			self.velocity += acceleration

			self.pos[0] += self.velocity.x
			self.pos[1] += self.velocity.y
			self.rect.center = self.pos

	def hitDetect(self):
		if self.pos[0] < 0 or self.pos[0] >= len(my.ENGINE.game.map.blocks):
			my.ENGINE.game.entities.remove(self)
			return True

		# HIT PLAYER
		collided = False
		for entity in my.ENGINE.game.getLiveEntities():
			if entity != self.shooter:
				if pygame.sprite.collide_rect(entity, self):
					collided = True
					entity.health -= self.DAMAGE
		self.firing = not collided
		if collided: return True

		# HIT GROUND
		x = int(self.pos[0])
		y = int(self.pos[1])
		if x > 0 and y > 0 and x < len(my.ENGINE.game.map.blocks) and y < len(my.ENGINE.game.map.blocks[x]):
			if my.ENGINE.game.map.blocks[x][y] != my.BLOCK_NONE:
				self.firing = False
				return True

		# HIT NOTHING
		return False
