"""

An simple user interface library object-oriented to pygame.

@author: Willian Gois
"""

import pygame

CENTER = 0x01
RIGHT = 0x02
LEFT = 0x03
UPPER = 0x04
BOTTOM = 0x05


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

