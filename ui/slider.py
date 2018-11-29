import pygame
from .widget import Widget
from .ui import CENTER, IMAGES


class SliderBar(Widget):

	def __init__(self, onchange, pos, size=[0, 0], min=0, max=100, step=1, initial=None, varType=int, image_slider=None, image_pointer=None, centralization=CENTER):
		Widget.__init__(self, pos, (max, image_slider.get_height()) if size[0] == 0 else size, centralization)
		self.onchange = onchange
		self.min = min
		self.max = max
		self.step = step
		self.value = min if initial is None else initial
		self.varType = varType
		self.image_slider = pygame.transform.scale(image_slider, self.size)
		self.image_pointer = image_pointer
		self.selected = True

	def get(self):
		return round(self.varType(self.value), 1)

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
		mouse = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if mouse in self:
				self.selected = True
		if event.type == pygame.MOUSEBUTTONUP:
			if self.selected:
				self.selected = False

		if self.selected:
			last_value = self.get()
			self.setPixelsToValue(mouse[0])

			if not self.get() == last_value:
				self.onchange(self.get())

	def render(self, screen):
		screen.blit(self.image_slider, self.pos)
		screen.blit(self.image_pointer, (
		self.getValueToPixel() - self.image_pointer.get_width() / 2, self.pos[1] - self.image_pointer.get_height() / 2))
