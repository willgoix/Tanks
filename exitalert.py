import pygame
from ui import ui, button, label
import my


class ExitAlert(ui.UI):
	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.background = pygame.Surface((my.SCREEN_WIDTH*2, my.SCREEN_HEIGHT*2))
		self.background.fill(my.CONCRETE)
		self.background.set_alpha(5)
		center = pygame.Surface((my.SCREEN_WIDTH/3, my.SCREEN_HEIGHT/2))
		center.fill((255, 255, 255))
		self.background.blit(center, (my.SCREEN_WIDTH, my.SCREEN_HEIGHT))

		self.addWidget(label.Image([0, 0], self.background))

		self.animation = True
		self.result = True

	def update(self, events):
		super().update(events)

		return self.result