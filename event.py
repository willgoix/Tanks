import pygame, my, exitalert
from sys import exit


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
		# TODO: Corrigir tamanho quando está em tela cheia

	def showConfirmExitAlert(self):
		my.ENGINE.interface = exitalert.ExitAlert(my.ENGINE.screen)

	def terminate(self):
		pygame.quit()
		exit()
