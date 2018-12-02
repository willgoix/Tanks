import pygame, my, sound
from os import listdir

IMAGES = {}


def loadImages(directory):
	for filename in listdir(directory):
		IMAGES[filename.split(".")[0]] = pygame.image.load('{}/{}'.format(directory, filename)).convert_alpha()


class Explosion(pygame.sprite.Sprite):

	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		my.ENGINE.game.entities.add(self)

		self.image = IMAGES['1']
		self.rect = self.image.get_rect()
		self.rect.x = pos[0] - 75
		self.rect.y = pos[1] - 156
		self.timer = 0

		sound.play('explode')
		self.removeBlocks()

	def removeBlocks(self):
		EXPLOSION_SIZE = 20

		x1 = self.rect.x - EXPLOSION_SIZE
		x2 = self.rect.x + EXPLOSION_SIZE
		y1 = my.SCREEN_HEIGHT - self.rect.y - EXPLOSION_SIZE
		y2 = my.SCREEN_HEIGHT - self.rect.y + EXPLOSION_SIZE
		for x in range(x1, x2):
			for y in range(y1, y2):
				if x < len(my.ENGINE.game.map.blocks) and y < len(my.ENGINE.game.map.blocks[x]):
					my.ENGINE.game.map.blocks[x][y] = my.BLOCK_NONE

		x1 = self.rect.x - EXPLOSION_SIZE
		x2 = self.rect.x + EXPLOSION_SIZE
		y1 = self.rect.y - EXPLOSION_SIZE
		y2 = self.rect.y + EXPLOSION_SIZE
		my.ENGINE.game.map.image.fill(my.BLOCK_COLORS[my.BLOCK_NONE], pygame.Rect((x1, y1), (x2 - x1, y2 - y1)))

	def update(self):
		self.timer += 1

		if self.timer >= 84:
			my.ENGINE.game.entities.remove(self)
		else:
			self.image = IMAGES[str(self.timer // 6)]
