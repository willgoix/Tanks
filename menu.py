import pygame, math, my, sound
from ui import ui, button, label


class Menu(ui.UI):
	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.logo = label.Image([my.SCREEN_WIDTH / 2, -my.SCREEN_HEIGHT], pygame.image.load("assets/logo.png"), centralization=ui.BOTTOM)
		self.addWidget(self.logo)

		self.playOfflineButton = button.ImageButton(lambda: self.playOffline(),
													[my.SCREEN_WIDTH / 2, my.SCREEN_HEIGHT],
													text="Jogar Offline",
													image_surface=ui.IMAGES['button'],
													image_pressed=ui.IMAGES['button_pressed'], )
		self.playOnlineButton = button.ImageButton(lambda: self.playOnline(),
												   [my.SCREEN_WIDTH / 2, my.SCREEN_HEIGHT],
												   text="Jogar Online",
												   image_surface=ui.IMAGES['button'],
												   image_pressed=ui.IMAGES['button_pressed'])
		self.optionsButton = button.ImageButton(lambda: self.playOnline(),
												[my.SCREEN_WIDTH / 2, my.SCREEN_HEIGHT],
												text="Opções",
												image_surface=ui.IMAGES['button'],
												image_pressed=ui.IMAGES['button_pressed'])
		self.creditsButton = button.ImageButton(lambda: self.credits(),
												[my.SCREEN_WIDTH / 2, my.SCREEN_HEIGHT],
												text="Créditos",
												image_surface=ui.IMAGES['button'],
												image_pressed=ui.IMAGES['button_pressed'])
		self.addWidget(self.playOfflineButton)
		self.addWidget(self.playOnlineButton)
		self.addWidget(self.optionsButton)
		self.addWidget(self.creditsButton)
		self.addWidget(label.Text([my.SCREEN_WIDTH - 5, my.SCREEN_HEIGHT], "Tanks 0.1 dev build", 24, centralization=ui.LEFT | ui.UPPER))

		self.animation = True
		self.readyToNext = False
		self.next = self

	def update(self, events):
		self.screen.fill((127, 140, 141))
		super().update(events)

		if self.animation:
			# TO UP
			y = 0
			for button in (self.playOfflineButton, self.playOnlineButton, self.optionsButton, self.creditsButton):
				if button.pos[1] > my.SCREEN_HEIGHT / 2 + y:
					button.pos[1] -= int(math.fabs(my.SCREEN_HEIGHT / 2 + y - button.pos[1]) * 0.1)
					y += 60

			# TO DOWN
			if self.logo.pos[1] < 0:
				self.logo.pos[1] += math.fabs(self.logo.pos[1]) * 0.1
		else:
			# TO UP
			y = 0
			for button in (self.playOfflineButton, self.playOnlineButton, self.optionsButton, self.creditsButton):
				if button.pos[1] < my.SCREEN_HEIGHT:
					button.pos[1] += (my.SCREEN_HEIGHT + y - button.pos[1]) * 0.1
					y += 60

			# TO DOWN
			if self.logo.pos[1] < 0:
				self.logo.pos[1] += math.fabs(self.logo.pos[1]) * 0.1

		return self.next

	def playOffline(self):
		sound.play('click')
		self.animation = False
		self.next = PlayOfflineMenu(self.screen)

	def playOnline(self):
		sound.play('click')
		self.animation = False

	def options(self):
		sound.play('click')
		self.animation = False

	def credits(self):
		sound.play('click')
		self.animation = False


class PlayOfflineMenu(ui.UI):

	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.addWidget(label.Text([100, 100], "Teste", 24))

		self.next = self

	def update(self, events):
		self.screen.fill((127, 140, 141))
		super().update(events)

		return self.next
