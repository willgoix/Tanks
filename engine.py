import pygame

pygame.mixer.pre_init(44100, 16, 2, 1024)
pygame.init()

import my, ui.ui, event, menu, sound, bullet, explosion


class Engine:

	def __init__(self):
		""" PRE-RUN """
		self.adaptScreen()
		pygame.display.set_icon(pygame.image.load('assets/tanks/tank_1.png'))
		pygame.display.set_caption("Tanks - Iniciando...")

		""" LOADING SCREEN """
		self.screen.fill(my.RED)
		text = my.FONT(24).render("Carregando...", True, (0, 0, 0))
		self.screen.blit(text, (my.SCREEN_HALF_WIDTH - text.get_size()[0] / 2, my.SCREEN_HALF_HEIGHT))
		pygame.display.update()

		self.game = None
		self.clock = None
		self.event_manager = None
		self.interface = None
		self.cursor = None
		self.running = True

	def run(self):
		pygame.display.init()
		pygame.font.init()

		ui.loadImages('assets/ui')
		bullet.loadImages('assets/bullets')
		explosion.loadImages('assets/explosion')
		sound.loadSounds('assets/sounds')

		self.clock = pygame.time.Clock()
		self.event_manager = event.EventManager()
		self.interface = menu.Menu(self.screen)
		self.cursor = ui.IMAGES['cursor']
		pygame.mouse.set_visible(False)

		while self.running:
			self.event_manager.get()
			self.interface = self.interface.update(self.event_manager.events)

			if self.game is not None:
				self.game.tick()

			self.screen.blit(self.cursor, pygame.mouse.get_pos())

			pygame.display.flip()
			self.clock.tick(my.FPS)
			pygame.display.set_caption("Tanks - v" + my.VERSION + " - FPS: " + str(round(self.clock.get_fps(), 1)))

	def adaptScreen(self):
		if my.WINDOWED:
			self.screen = pygame.display.set_mode((my.SCREEN_WIDTH, my.SCREEN_HEIGHT))  # , pygame.NOFRAME)
		else:
			self.screen = pygame.display.set_mode((my.SCREEN_WIDTH, my.SCREEN_HEIGHT),
												  pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF if my.HARDWARE_ACCELERATED else pygame.FULLSCREEN)

	def setCursor(self, cursor):
		if cursor != self.cursor:
			self.cursor = cursor


if __name__ == '__main__':
	my.ENGINE = Engine()
	my.ENGINE.run()
