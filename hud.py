import pygame, math, my, sound, game
from ui import ui, label, bar
from functools import partial

class Hud(ui.UI):

	def __init__(self, game, screen):
		ui.UI.__init__(self, screen)
		self.game = game
		self.playersWidgets = {}

		''' LEFT BAR '''
		# TODO: Seleção de munição
		panel = pygame.transform.scale(ui.IMAGES['metal_panel'], (250, 150))
		self.addWidget(label.Image([10, 10], panel, centralization=ui.RIGHT | ui.BOTTOM))

		self.timer = label.Text([60, 25], 'Próximo turno: 00', fontsize=15, centralization=ui.RIGHT | ui.BOTTOM)
		self.addWidget(self.timer)

		self.fuel = bar.Bar([panel.get_size()[0] / 2 + 10, 60],
						size=[panel.get_size()[0] - 60, 15],
						min=0, max=100, initial=100,
						image_bar_left=ui.IMAGES['bar_yellow_left'],
						image_bar_mid=ui.IMAGES['bar_yellow_mid'],
						image_bar_right=ui.IMAGES['bar_yellow_right'])
		self.addWidget(self.fuel)
		self.addWidget(label.Text([panel.get_size()[0] // 5, 54], 'Combustível', centralization=ui.RIGHT | ui.BOTTOM))

		''' RIGHT BAR '''
		panelLife = pygame.transform.scale(ui.IMAGES['metal_panel'], (250, len(self.game.getLiveEntities()) * 20 + 60))
		self.addWidget(label.Image([my.SCREEN_WIDTH - 10, 10], panelLife, centralization=ui.LEFT | ui.BOTTOM))
		self.addWidget(label.Text([my.SCREEN_WIDTH - 65, 25], 'Vida dos jogadores', centralization=ui.LEFT | ui.BOTTOM))

		y = 40
		for entity in self.game.getLiveEntities():
			y += 20
			self.playersWidgets[entity.id] = [
				label.Text([entity.pos[0], entity.pos[1] - 50], entity.nickname, high=True),

				bar.Bar([entity.pos[0], entity.pos[1] - 40],
						size=[entity.image.get_width(), 20],
						min=0, max=entity.health, initial=entity.health,
						image_bar_left=ui.IMAGES['bar_red_left'],
						image_bar_mid=ui.IMAGES['bar_red_mid'],
						image_bar_right=ui.IMAGES['bar_red_right']),

				bar.Bar([my.SCREEN_WIDTH - panelLife.get_size()[0] / 2 - 10, y],
						size=[panelLife.get_size()[0] - 60, 15],
						min=0, max=entity.health, initial=entity.health,
						image_bar_left=ui.IMAGES['bar_red_left'],
						image_bar_mid=ui.IMAGES['bar_red_mid'],
						image_bar_right=ui.IMAGES['bar_red_right'])]

			#self.addWidget(self.playersWidgets[entity.id][0])
			#self.addWidget(self.playersWidgets[entity.id][1])
			self.addWidget(self.playersWidgets[entity.id][2])

			self.addWidget(label.Text([my.SCREEN_WIDTH - panelLife.get_size()[0] + 25, y - 7], entity.nickname,
									  centralization=ui.RIGHT | ui.BOTTOM))

		self.next = self

	def removeWidgets(self, entity):
		for widget in self.playersWidgets[entity.id]:
			if widget in self.widgets:
				self.removeWidget(widget)
		del self.playersWidgets[entity.id]

	def update(self, events):
		self.timer.text = 'Próximo turno: ' + str(self.game.turncontroller.timer)
		# FUEL BAR IN RIGHT PANEL
		self.fuel.value = self.game.player.fuel if self.game.player.fuel >= 0 else 0

		for entity in self.game.getLiveEntities():
			""" É necessário adaptar a posição levando em relação o scroll da tela
			# NICKNAME
			self.playersWidgets[entity.id][0].pos = [entity.pos[0] - (
				len(entity.nickname) if len(entity.nickname) == 6 else (
					len(entity.nickname) * 2 if len(entity.nickname) > 6 else 0)), entity.pos[1] - 50]

			# HEALTH BAR
			self.playersWidgets[entity.id][1].pos = [entity.pos[0], entity.pos[1] - 35]
			self.playersWidgets[entity.id][1].value = entity.health
			"""

			# HEALTH BAR IN LEFT PANEL
			self.playersWidgets[entity.id][2].value = entity.health

		ui.UI.update(self, events)


		return self.next
