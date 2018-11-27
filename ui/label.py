from my import FONT, FONT_HIGH
from .widget import Widget
from .ui import CENTER


class Text(Widget):

	def __init__(self, pos, text, fontsize=12, high=False, centralization=CENTER):
		Widget.__init__(self, pos, FONT_HIGH(fontsize).size(text) if high else FONT(fontsize).size(text), centralization)
		self.text = text
		self.font = FONT_HIGH(fontsize) if high else FONT(fontsize)

	def update(self, event):
		pass

	def render(self, screen):
		screen.blit(self.font.render(self.text, True, (0, 0, 0)), self.pos)


class Image(Widget):

	def __init__(self, pos, image, centralization=CENTER):
		Widget.__init__(self, pos, image.get_size(), centralization)
		self.image = image

	def update(self, event):
		pass

	def render(self, screen):
		screen.blit(self.image, self.pos)
