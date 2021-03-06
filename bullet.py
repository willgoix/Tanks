import pygame, my, explosion, math, random, sound, threading, os, lib.delayedfunc

IMAGES = {}


def loadImages(directory):
	for filename in os.listdir(directory):
		image = pygame.image.load('{}/{}'.format(directory, filename)) #TODO: Repôr .convert()
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

		self.pos = [pos[0] + (self.image.get_width() if pygame.mouse.get_pos()[0] > pos[0] else -self.image.get_width()), pos[1]]
		self.rect = self.image.get_rect(center=self.pos)
		self.rect.x += self.rect.w if pygame.mouse.get_pos()[0] > pos[0] else -self.rect.w

		self.velocity = velocity
		self.shooter = shooter
		self.firing = True
		self.DAMAGE = random.randrange(15, 20)

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
			explosion.Explosion(self.pos)
			my.ENGINE.game.entities.remove(self)

			lib.delayedfunc.DelayedFunc(lambda: my.ENGINE.game.turncontroller.next(), 2)
		else:
			acceleration = my.GRAVITY + my.ENGINE.game.wind.wind
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
