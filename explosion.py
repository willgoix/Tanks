import pygame, my, sound, math
from os import listdir

IMAGES = {}


def loadImages(directory):
	for filename in listdir(directory):
		IMAGES[filename.split(".")[0]] = pygame.image.load('{}/{}'.format(directory, filename)).convert_alpha()


class Explosion(pygame.sprite.Sprite):

	def __init__(self, pos, size=30):
		pygame.sprite.Sprite.__init__(self)
		my.ENGINE.game.entities.add(self)

		self.image = IMAGES['1']
		self.rect = self.image.get_rect()
		self.rect.x = pos[0] - 75
		self.rect.y = pos[1] - 156
		self.pos = (int(pos[0]), int(pos[1]))

		self.size = size
		self.timer = 0

		sound.play('explode')
		self.removeBlocks()

	def removeBlocks(self):
		"""
			The equation of a circle with center (h,k) and radius r units is (x−h)2+(y−k)2=r2
			https://www.varsitytutors.com/hotmath/hotmath_help/topics/equation-of-a-circle
		"""
		
		x1 = self.pos[0] - self.size
		x2 = self.pos[0] + self.size
		y1 =  self.pos[1] - self.size
		y2 = self.pos[1] + self.size

		for x in range(x1, x2):
			for y in range(y1, y2):
				if math.sqrt((x-self.pos[0])**2 + (y-self.pos[1])**2) <= self.size:
					if x < len(my.ENGINE.game.map.blocks) and x > 0 and y < len(my.ENGINE.game.map.blocks[0]) and y > 0:
						my.ENGINE.game.map.blocks[x][y] = my.BLOCK_NONE
						my.ENGINE.game.map.image.set_at((x, y), my.BLOCK_COLORS[my.BLOCK_NONE])

	def update(self):
		self.timer += 1

		if self.timer >= 84:
			my.ENGINE.game.entities.remove(self)
		else:
			self.image = IMAGES[str(self.timer // 6)]
