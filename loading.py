import pygame, my
from ui import ui, label, bar


class Loading(ui.UI):

	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.text = label.Text(my.SCREEN_HALF_SIZE, 'Gerando mapa...', fontsize=20)
		self.bar = bar.Bar([my.SCREEN_HALF_HEIGHT+100, my.SCREEN_HALF_HEIGHT+30], size=[400, 20],
							min=0, max=100, initial=1,
							image_bar_left=ui.IMAGES['bar_red_left'],
							image_bar_mid=ui.IMAGES['bar_red_mid'],
							image_bar_right=ui.IMAGES['bar_red_right'])

		self.addWidget(self.text)
		self.addWidget(self.bar)

		self.next = self

	def setStatus(self, status, value):
		self.text.text = status
		self.bar.value = value

	def update(self, events):
		self.screen.fill(my.RED)
		ui.UI.update(self, events)

		return self.next
