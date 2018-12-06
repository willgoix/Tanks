import pygame, my, exitalert

class EventManager:

	def __init__(self):
		self.clicked = False
		self.events = []

	def get(self):
		self.events = pygame.event.get()
		for event in self.events:
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.showConfirmExitAlert()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
				my.WINDOWED = not my.WINDOWED
				my.ENGINE.adaptScreen()

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.clicked = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.clicked = False

	def showConfirmExitAlert(self):
		my.ENGINE.interface = exitalert.ExitAlert(my.ENGINE.screen, my.ENGINE.interface)