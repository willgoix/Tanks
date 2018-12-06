import pygame, my
from .widget import Widget
from .ui import CENTER, IMAGES


class Bar(Widget):

	def __init__(self, pos, size=[0, 0], min=0, max=100, initial=None, image_bar_left=None, image_bar_mid=None, image_bar_right=None):
		Widget.__init__(self, pos, size, CENTER)
		self.min = min
		self.max = max
		self.value = min if initial is None else initial

		self.image_bar_left = pygame.transform.scale(image_bar_left, (5, size[1]))
		self.image_bar_mid = pygame.transform.scale(image_bar_mid, (1, size[1]))
		self.image_bar_right = pygame.transform.scale(image_bar_right, (5, size[1]))

		self.image_shadow_left = pygame.transform.scale(IMAGES['bar_shadow_left'], (5, size[1]))
		self.image_shadow_mid = pygame.transform.scale(IMAGES['bar_shadow_mid'], (1, size[1]))
		self.image_shadow_right = pygame.transform.scale(IMAGES['bar_shadow_right'], (5, size[1]))

		self.selected = True

	def get(self):
		return round(self.value, 1)

	def set(self, value):
		self.value = min(self.max, max(self.min, value))

	def getValueToPixel(self):
		step = self.size[0] / (self.max - self.min)
		return self.pos[0] + step * (self.value - self.min)

	def setPixelsToValue(self, value):
		value = min(self.pos[0] + self.size[0], max(self.pos[0], value))

		delta_x = value - self.pos[0]
		prop = delta_x / self.size[0]
		real = prop * (self.max - self.min)
		self.value = self.min + round(real / self.step) * self.step

	def update(self, event):
		pass

	def render(self, screen):
		differencePx = int(self.getValueToPixel() - self.pos[0])
		rest = int((self.pos[0] + self.size[0]) - self.getValueToPixel())

		x = 0
		for i in range(0, differencePx):
			image = self.image_bar_mid
			if i == 0:
				image = self.image_bar_left
			elif i == differencePx-1:
				image = self.image_bar_right

			screen.blit(image, (self.pos[0] + x, self.pos[1]))
			x += 1

		for i in range(0, rest):
			image = self.image_shadow_mid
			if differencePx == 0:
				image = self.image_shadow_left
			elif i == rest-1:
				image = self.image_shadow_right

			screen.blit(image, (self.pos[0] + x, self.pos[1]))
			x += 1

