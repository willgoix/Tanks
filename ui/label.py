from my import FONT, FONT_HIGH
from .widget import Widget


def Text(Widget):

	def __init__(self, pos, text, fontsize=12, high=False):
		Widget.__init__(self, pos, FONT_HIGH(fontsize).size(text) if high else FONT(fontsize).size(text))
		self.text = text
		self.font = FONT_HIGH(fontsize) if high else FONT(fontsize)

	def update(self, event):
		pass

	def render(self, screen):
		pass
