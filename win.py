import pygame, my
from ui import ui, label, bar


class Win(ui.UI):

	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.text = label.Text(my.SCREEN_HALF_SIZE, 'Vencedor!', fontsize=20)
		self.addWidget(self.bar)

		self.next = self

	def update(self, events):
		self.screen.fill(my.RED)
		ui.UI.update(self, events)

		return self.next
