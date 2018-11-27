import pygame
from ui import ui, button, label
import my


class ExitAlert(ui.UI):
	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.background = pygame.Surface((my.SCREEN_WIDTH, my.SCREEN_HEIGHT))
		self.background.fill(my.CONCRETE)
		self.background.set_alpha(50)

		self.addWidget(label.Image([0, 0], self.background))

		self.animation = True
		self.result = True

	def update(self, events):
		self.screen.blit(self.background, (0, 0))
		super().update(events)

		return self.result