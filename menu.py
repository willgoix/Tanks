import pygame, math, my, sound
from ui import ui, button, label, slider
from functools import partial


class Menu(ui.UI):
	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.logo = label.Image([my.SCREEN_HALF_WIDTH, -my.SCREEN_HEIGHT], pygame.image.load("assets/logo.png"),
								centralization=ui.BOTTOM)
		self.addWidget(self.logo)

		self.playOfflineButton = button.ImageButton(lambda: self.playOffline(),
													[my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
													text="Jogar Offline",
													image_surface=ui.IMAGES['button'],
													image_pressed=ui.IMAGES['button_pressed'], )
		self.playOnlineButton = button.ImageButton(lambda: self.playOnline(),
												   [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
												   text="Jogar Online",
												   image_surface=ui.IMAGES['button'],
												   image_pressed=ui.IMAGES['button_pressed'])
		self.optionsButton = button.ImageButton(lambda: self.options(),
												[my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
												text="Opções",
												image_surface=ui.IMAGES['button'],
												image_pressed=ui.IMAGES['button_pressed'])
		self.creditsButton = button.ImageButton(lambda: self.credits(),
												[my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
												text="Créditos",
												image_surface=ui.IMAGES['button'],
												image_pressed=ui.IMAGES['button_pressed'])
		self.addWidget(self.playOfflineButton)
		self.addWidget(self.playOnlineButton)
		self.addWidget(self.optionsButton)
		self.addWidget(self.creditsButton)
		self.addWidget(label.Text([my.SCREEN_WIDTH - 5, my.SCREEN_HEIGHT], "Tanks v" + my.VERSION, 20,
								  centralization=ui.LEFT | ui.UPPER))

		self.animation = True
		self.readyToNext = False
		self.next = self

	def update(self, events):
		# self.screen.blit(ui.IMAGES['background'], (0, 0))
		self.screen.fill(my.RED)
		super().update(events)

		if self.animation:
			# TO UP
			y = 0
			for button in (self.playOfflineButton, self.playOnlineButton, self.optionsButton, self.creditsButton):
				if button.pos[1] > my.SCREEN_HALF_HEIGHT + y:
					button.pos[1] -= int(math.fabs(my.SCREEN_HALF_HEIGHT + y - button.pos[1]) * 0.1)
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
		self.next = PlayOnlineMenu(self.screen)

	def options(self):
		sound.play('click')
		self.animation = False
		self.next = OptionsMenu(self.screen)

	def credits(self):
		sound.play('click')
		self.animation = False
		self.next = CreditsMenu(self.screen)


class PlayOfflineMenu(ui.UI):

	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.addWidget(label.Text(my.SCREEN_HALF_SIZE, "Em desenvolvimento...", fontsize=24))
		self.addWidget(button.ImageButton(lambda: self.back(),
										  [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT - 100],
										  text="Voltar",
										  image_surface=ui.IMAGES['button'],
										  image_pressed=ui.IMAGES['button_pressed']))

		self.addWidget(button.Drop(self, ['XXXXXXXXXXXXXXX', 'botao 2'], partial(self.select),
								   [my.SCREEN_HALF_WIDTH, 100],
								   text="Infos",
								   image_surface=ui.IMAGES['button'],
								   image_pressed=ui.IMAGES['button_pressed'],
								   down=True))

		self.next = self

	def update(self, events):
		self.screen.fill(my.RED)
		super().update(events)

		return self.next

	def back(self):
		self.next = Menu(self.screen)

	def select(self, content):
		print(content, " selected")


class PlayOnlineMenu(ui.UI):

	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.addWidget(label.Text(my.SCREEN_HALF_SIZE, "Em desenvolvimento...", fontsize=24))
		self.addWidget(button.ImageButton(lambda: self.back(),
										  [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT - 100],
										  text="Voltar",
										  image_surface=ui.IMAGES['button'],
										  image_pressed=ui.IMAGES['button_pressed']))

		self.next = self

	def update(self, events):
		self.screen.fill(my.RED)
		super().update(events)

		return self.next

	def back(self):
		self.next = Menu(self.screen)


class OptionsMenu(ui.UI):

	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.fpsValue = label.Text([my.SCREEN_HALF_WIDTH + 25, 60], str(my.FPS), fontsize=20)
		self.addWidget(self.fpsValue)
		self.addWidget(label.Text([my.SCREEN_HALF_WIDTH - 25, 60], "FPS", fontsize=20))
		self.addWidget(
			slider.SliderBar(partial(self.sliderFps), [my.SCREEN_HALF_WIDTH, 100], (300, 5), min=20, max=100, step=1,
							 initial=my.FPS,
							 image_slider=ui.IMAGES['slider'],
							 image_pointer=ui.IMAGES['slider_pointer']))

		self.addWidget(button.ImageButton(lambda: self.back(),
										  [my.SCREEN_HALF_WIDTH - 20, my.SCREEN_HEIGHT - 100],
										  text="Voltar",
										  image_surface=ui.IMAGES['button'],
										  image_pressed=ui.IMAGES['button_pressed'],
										  centralization=ui.LEFT))
		self.addWidget(button.ImageButton(lambda: self.save(),
										  [my.SCREEN_HALF_WIDTH + 20, my.SCREEN_HEIGHT - 100],
										  text="Salvar",
										  image_surface=ui.IMAGES['button_green'],
										  image_pressed=ui.IMAGES['button_green_pressed'],
										  centralization=ui.RIGHT))
		self.next = self

	def update(self, events):
		self.screen.fill(my.RED)
		super().update(events)

		return self.next

	def sliderFps(self, value):
		self.fpsValue.text = str(value)
		my.CONFIG.set('fps', value)

	def back(self):
		self.next = Menu(self.screen)

	def save(self):
		self.next = Menu(self.screen)
		my.FPS = my.CONFIG.get('fps')
		my.CONFIG.save()


class CreditsMenu(ui.UI):

	def __init__(self, screen):
		ui.UI.__init__(self, screen)

		self.addWidget(label.Text([200, 100], "Desenvolvido por:", fontsize=24, centralization=ui.RIGHT))
		self.addWidget(label.Text([250, 140], "Willian Gois ~the coder guy", fontsize=20, centralization=ui.RIGHT))
		self.addWidget(label.Text([250, 160], "Lucas Verona ~the h4ck3r m4n", fontsize=20, centralization=ui.RIGHT))

		self.addWidget(label.Text([200, 210], "Texturas por:", fontsize=24, centralization=ui.RIGHT))
		self.addWidget(
			label.Text([250, 250], "(UI): Kenney Vleugels (www.kenney.nl)", fontsize=20, centralization=ui.RIGHT))

		self.addWidget(button.ImageButton(lambda: self.back(),
										  [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT - 100],
										  text="Voltar",
										  image_surface=ui.IMAGES['button'],
										  image_pressed=ui.IMAGES['button_pressed']))

		self.next = self

	def update(self, events):
		self.screen.fill(my.RED)
		super().update(events)

		return self.next

	def back(self):
		self.next = Menu(self.screen)
