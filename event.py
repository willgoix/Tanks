import pygame, my, exitalert
from sys import exit


class EventManager:
	def __init__(self):
		self.events = []

	def get(self):
		self.events = pygame.event.get()
		for event in self.events:
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				self.showConfirmExitAlert()

			if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
				my.WINDOWED = not my.WINDOWED
				my.ENGINE.adaptScreen()
		# TODO: Corrigir tamanho quando está em tela cheia

	def showConfirmExitAlert(self):
		alertOpen = True
		alert = exitalert.ExitAlert(my.ENGINE.screen)
		while alertOpen:
			self.get()
			alertOpen = alert.update(self.events)

	def terminate(self):
		pygame.quit()
		exit()
