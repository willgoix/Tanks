import pygame, my, event, menu, ui.ui, sound


class Engine:

	def __init__(self):
		""" PRE-RUN """
		pygame.init()
		self.adaptScreen()
		# pygame.display.set_icon(pygame.image.load('assets/tanks/tank_desert.png'))
		pygame.display.set_caption("Tanks - Iniciando...")

		""" LOADING SCREEN """
		self.screen.fill(my.MIDNIGHT_BLUE)
		pygame.display.update()

		self.clock = None
		self.event_manager = None
		self.interface = None
		self.running = True

	def adaptScreen(self):
		if my.WINDOWED:
			self.screen = pygame.display.set_mode((my.SCREEN_WIDTH, my.SCREEN_HEIGHT)) #, pygame.NOFRAME)
		else:
			screenInfo = pygame.display.Info()
			my.SCREEN_WIDTH = screenInfo.current_w
			my.SCREEN_HEIGHT = screenInfo.current_h
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

	def run(self):
		pygame.display.init()
		pygame.font.init()
		pygame.mixer.pre_init(44100, -16, 2, 1024)

		ui.loadImages('assets/ui')
		sound.loadSounds('assets/sounds')

		self.clock = pygame.time.Clock()
		self.event_manager = event.EventManager()
		self.interface = menu.Menu(self.screen)

		while self.running:
			self.event_manager.get()
			self.interface = self.interface.update(self.event_manager.events)
			pygame.display.flip()

			self.clock.tick(my.FPS)
			pygame.display.set_caption("Tanks - FPS: ", str(self.clock.get_fps()))


if __name__ == '__main__':
	my.ENGINE = Engine()
	my.ENGINE.run()
