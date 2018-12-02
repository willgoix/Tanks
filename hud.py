import pygame, math, my, sound, game
from ui import ui, label, bar
from functools import partial


class Hud(ui.UI):

	def __init__(self, game, screen):
		ui.UI.__init__(self, screen)
		self.game = game
		self.playersWidgets = {}

		for entity in self.game.getLiveEntities():
			self.playersWidgets[entity.id] = [
				label.Text([entity.pos[0], entity.pos[1]], entity.nickname, high=True),

				bar.Bar([entity.pos[0], entity.pos[1] - 40], size=[entity.image.get_width(), 20],
						min=0, max=entity.health, initial=entity.health,
						image_bar_left=ui.IMAGES['bar_red_left'],
						image_bar_mid=ui.IMAGES['bar_red_mid'],
						image_bar_right=ui.IMAGES['bar_red_right'])]

			self.addWidget(self.playersWidgets[entity.id][0])
			self.addWidget(self.playersWidgets[entity.id][1])

		self.next = self

	def removeWidgets(self, entity):
		for widget in self.playersWidgets[entity.id]:
			self.removeWidget(widget)
		del self.playersWidgets[entity.id]

	def update(self, events):
		self.screen.fill((255, 255, 255))

		for entity in self.game.getLiveEntities():
			self.playersWidgets[entity.id][0].pos = [entity.rect.x, entity.rect.y - 50]

			self.playersWidgets[entity.id][1].pos = [entity.rect.x, entity.rect.y - 40]
			self.playersWidgets[entity.id][1].value = entity.health

		ui.UI.update(self, events)

		return self.next
