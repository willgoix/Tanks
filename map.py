import pygame, my, random, math, lib.delayedfunc
import lib.opensimplex as opensimplex

FREQUENCY = 5  # elevaçao/zoom, maior = menos distancia entre as ilhas
OCTAVES = 2  # deixa menos redondo/suave
REDISTRIBUTION = 1


class Map(pygame.sprite.Sprite):

	def __init__(self, width, height, seed):
		pygame.sprite.Sprite.__init__(self)
		self.width = width
		self.height = height

		image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
		self.image = image.convert_alpha()
		self.rect = self.image.get_rect()

		self.blocks = [[my.BLOCK_NONE for y in range(self.height)] for x in range(self.width)]
		self.generator = opensimplex.OpenSimplex(seed)

	def generate(self):
		for x in range(0, self.width):
			my.ENGINE.game.hud.setStatus('Gerando mapa...', my.ENGINE.game.hud.bar.value + 0.1)
			for y in range(0, 1):
				noise = self.__generateNoise(x, y, self.width, self.height)

				self.drawColumn(x, int(noise * 200) + self.height // 2 + 50)

		self.image.set_alpha(150)

	def drawColumn(self, xx, y):
		for yy in range(self.height, y, -1):
			if xx >= self.width or xx < 0 or yy >= self.height or yy < 0:
				continue

			block = my.BLOCK_ROCK
			if yy <= y + 20:
				block = my.BLOCK_GRASS
			elif yy <= y + 80:
				block = my.BLOCK_DIRT

			self.image.set_at((xx, yy), my.BLOCK_COLORS[block])
			self.blocks[xx][yy] = block



	def getMaxHeight(self, x):
		column = self.blocks[x]

		for y in range(self.height - 1, 0, -1):
			if column[y] == my.BLOCK_NONE:
				return y + 1

		return self.height

	def __getBlockByNoise(self, noise):
		if noise < 0:
			return my.BLOCK_ROCK
		elif noise < 0.2:
			return my.BLOCK_DIRT
		elif noise < 0.4:
			return my.BLOCK_GRASS
		else:
			return my.BLOCK_NONE

	def __noise(self, nx, ny):
		# Rescale from -1.0 : +1.0 to 0.0 : 1.0
		return self.generator.noise2d(nx, ny)  # / 2.0 + 0.5

	def __generateNoise(self, x, y, width, height):
		nx = x / width - 0.5
		ny = y / height - 0.5
		nois = 0

		freq = FREQUENCY
		for i in range(OCTAVES, 0, -1):
			nois += (i / OCTAVES) * self.__noise(nx * freq, ny * freq)
			freq *= 2

		return pow(nois, REDISTRIBUTION)
