"""

An simple user interface library object-oriented to pygame.

@author: Willian Gois
"""

import pygame
from os import listdir

""" BITMASK CENTRALIZATIONS """
CENTER = 0x00
RIGHT = 0x01
LEFT = 0x02
UPPER = 0x04
BOTTOM = 0x08

IMAGES = {}


def loadImages(directory):
	for filename in listdir(directory):
		image = pygame.image.load('{}/{}'.format(directory, filename)).convert()
		image.set_colorkey((0, 0, 0))
		IMAGES[filename.split(".")[0]] = image


class UI:
	def __init__(self, screen):
		self.screen = screen
		self.widgets = []

	def __contains__(self, item):
		return item in self.widgets

	def __del__(self):
		self.widgets.clear()

	def addWidget(self, widget):
		self.widgets.append(widget)
		widget.render(self.screen)

	def update(self, events):
		for widget in self.widgets:
			for event in events:
				if hasattr(event, 'pos'):
					widget.update(event)
			widget.render(self.screen)
