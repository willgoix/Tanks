import pygame

pygame.mixer.pre_init(44100, 16, 2, 1024)
pygame.init()

import my, ui.ui, event, menu, sound


class Engine:

	def __init__(self):
		""" PRE-RUN """
		self.adaptScreen()
		# pygame.display.set_icon(pygame.image.load('assets/tanks/tank_desert.png'))
		pygame.display.set_caption("Tanks - Iniciando...")

		""" LOADING SCREEN """
		self.screen.fill(my.RED)
		text = my.FONT(24).render("Carregando...", True, (0, 0, 0))
		self.screen.blit(text, (my.SCREEN_HALF_WIDTH - text.get_size()[0] / 2, my.SCREEN_HALF_HEIGHT))
		pygame.display.update()

		self.clock = None
		self.event_manager = None
		self.interface = None
		self.cursor = None
		self.running = True

	def adaptScreen(self):
		if my.WINDOWED:
			self.screen = pygame.display.set_mode((my.SCREEN_WIDTH, my.SCREEN_HEIGHT))  # , pygame.NOFRAME)
		else:
			screenInfo = pygame.display.Info()
			my.SCREEN_WIDTH = screenInfo.current_w
			my.SCREEN_HEIGHT = screenInfo.current_h
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

	def setCursor(self, cursor):
		if cursor != self.cursor:
			self.cursor = cursor

	def run(self):
		pygame.display.init()
		pygame.font.init()

		ui.loadImages('assets/ui')
		sound.loadSounds('assets/sounds')

		self.clock = pygame.time.Clock()
		self.event_manager = event.EventManager()
		self.interface = menu.Menu(self.screen)
		self.cursor = ui.IMAGES['cursor']
		pygame.mouse.set_visible(False)

		while self.running:
			self.event_manager.get()
			self.interface = self.interface.update(self.event_manager.events)
			self.screen.blit(self.cursor, pygame.mouse.get_pos())

			pygame.display.flip()
			self.clock.tick(my.FPS)
			pygame.display.set_caption("Tanks - v" + my.VERSION + " - FPS: " + str(round(self.clock.get_fps(), 1)))


if __name__ == '__main__':
	my.ENGINE = Engine()
	my.ENGINE.run()
