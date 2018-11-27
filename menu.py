import pygame, math
from ui import ui, button, label
import my


class Menu(ui.UI):
	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		logo = pygame.image.load("assets/logo.jpg").convert()
		logo.set_colorkey((0, 0, 0))
		self.addWidget(label.Image([my.SCREEN_WIDTH / 2, 0], logo))

		self.playOfflineButton = button.ImageButton(lambda: self.playOffline(),
													[my.SCREEN_WIDTH / 2, my.SCREEN_HEIGHT],
													text="Jogar Offline",
													image_surface=ui.IMAGES['button'],
													image_pressed=ui.IMAGES['button_pressed'],
													centralization=ui.LEFT)
		self.playOnlineButton = button.ImageButton(lambda: self.playOnline(),
												   [my.SCREEN_WIDTH / 2, my.SCREEN_HEIGHT],
												   text="Jogar Online",
												   image_surface=ui.IMAGES['button'],
												   image_pressed=ui.IMAGES['button_pressed'],
												   centralization=ui.RIGHT)
		self.optionsButton = button.ImageButton(lambda: self.playOnline(),
												[my.SCREEN_WIDTH / 2, my.SCREEN_HEIGHT],
												text="Opções",
												image_surface=ui.IMAGES['button'],
												image_pressed=ui.IMAGES['button_pressed'])
		self.creditsButton = button.ImageButton(lambda: self.credits(),
												[my.SCREEN_WIDTH / 2,  my.SCREEN_HEIGHT],
												text="Créditos",
												image_surface=ui.IMAGES['button'],
												image_pressed=ui.IMAGES['button_pressed'])
		self.addWidget(self.playOfflineButton)
		self.addWidget(self.playOnlineButton)
		self.addWidget(self.optionsButton)
		self.addWidget(self.creditsButton)
		self.addWidget(label.Text([my.SCREEN_WIDTH-5, my.SCREEN_HEIGHT], "Tanks 0.1 dev build", 24, centralization=ui.LEFT | ui.UPPER))

		self.animation = True
		self.next = self

	def update(self, events):
		self.screen.fill(my.MIDNIGHT_BLUE)
		super().update(events)

		if self.animation:
			y = 0
			for button in (self.playOfflineButton, self.playOfflineButton, self.optionsButton, self.creditsButton):
				if button.pos[1] > my.SCREEN_HEIGHT / 2 + y:
					button.pos[1] -= math.fabs(my.SCREEN_HEIGHT / 2 + y - button.pos[1]) * 0.1
					y += 60

		# if self.playOfflineButton.pos[1] > my.SCREEN_HEIGHT / 2 + 50:
		#	self.playOfflineButton.pos[1] -= math.fabs(my.SCREEN_HEIGHT / 2 + 300 - self.playOfflineButton.pos[1]) * 0.1

		# if self.playOnlineButton.pos[1] > my.SCREEN_HEIGHT / 2 + 50:
		#	self.playOnlineButton.pos[1] -= math.fabs(my.SCREEN_HEIGHT / 2 + 300 - self.playOnlineButton.pos[1]) * 0.1

		# if self.optionsButton.pos[1] > my.SCREEN_HEIGHT / 2:
		#	self.optionsButton.pos[1] -= math.fabs(my.SCREEN_HEIGHT / 2 + 300 - self.optionsButton.pos[1]) * 0.1

		# if self.creditsButton.pos[1] > my.SCREEN_HEIGHT / 2:
		#	self.creditsButton.pos[1] -= math.fabs(my.SCREEN_HEIGHT / 2 + 300 - self.creditsButton.pos[1]) * 0.1
		else:
			if self.playOfflineButton.pos[1] < my.SCREEN_HEIGHT - 1:
				self.playOfflineButton.pos[1] += (my.SCREEN_HEIGHT + 50 - self.playOfflineButton.pos[1]) * 0.1

			if self.playOnlineButton.pos[1] < my.SCREEN_HEIGHT - 1:
				self.playOnlineButton.pos[1] += (my.SCREEN_HEIGHT + 50 - self.playOnlineButton.pos[1]) * 0.1

			if self.optionsButton.pos[1] < my.SCREEN_HEIGHT - 1:
				self.optionsButton.pos[1] += (my.SCREEN_HEIGHT + 50 - self.optionsButton.pos[1]) * 0.1

			if self.creditsButton.pos[1] < my.SCREEN_HEIGHT - 1:
				self.creditsButton.pos[1] += (my.SCREEN_HEIGHT + 50 - self.creditsButton.pos[1]) * 0.1

		return self.next

	def playOffline(self):
		import sound
		sound.play('click')
		self.animation = False

	def playOnline(self):
		self.animation = False

	def options(self):
		self.animation = False

	def credits(self):
		self.animation = False
