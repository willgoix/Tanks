"""

An simple user interface library object-oriented to pygame.

@author: Willian Gois
"""

import pygame, os

""" BITMASK CENTRALIZATIONS """
CENTER = 0x00
RIGHT = 0x01
LEFT = 0x02
UPPER = 0x04
BOTTOM = 0x08

IMAGES = {}


def loadImages(directory):
    for filename in os.listdir(directory):
        image = pygame.image.load('{}/{}'.format(directory, filename)) #TODO: Repôr .convert()
        IMAGES[filename.split(".")[0]] = image


class UI:

    def __init__(self, screen):
        self.screen = screen
        self.widgets = []

    def __contains__(self, item):
        return item in self.widgets

    def __del__(self):
        self.widgets.clear()

    def removeWidget(self, widget):
        self.widgets.remove(widget)

    def addWidget(self, widget):
        self.widgets.append(widget)
        widget.render(self.screen)

    def update(self, events):
        for widget in self.widgets:
            for event in events:
                if hasattr(event, 'pos'):
                    widget.update(event)
                    continue

                if widget.__module__ == 'ui.input':
                    if event.type == pygame.KEYDOWN:
                        widget.update(event)
            widget.render(self.screen)
