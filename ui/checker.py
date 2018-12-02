import pygame
from .widget import Widget
from .ui import CENTER


class Checker(Widget):

	def __init__(self, onselect, pos, size=[0, 0], checked=False, image=None, image_checked=None, centralization=CENTER):
		Widget.__init__(self, pos, image.get_size() if size[0] == 0 else size, centralization)
		self.onselect = onselect
		self.image = pygame.transform.smoothscale(image, self.size)
		self.image_selected = pygame.transform.smoothscale(image_checked, self.size)

		self.checked = checked

	def update(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos in self:
				self.checked = not self.checked
				self.onselect(self.checked)

	def render(self, screen):
		screen.blit(self.image_selected if self.checked else self.image, self.pos)