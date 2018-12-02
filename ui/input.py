import pygame, my
from .widget import Widget
from .ui import CENTER


class TextBox(Widget):

	def __init__(self, oninput, pos, size=[0, 0], pretext='', fontsize=12, box_image=None, centralization=CENTER):
		Widget.__init__(self, pos, size if not size[0] == 0 else my.FONT(fontsize).size(pretext), centralization)
		self.oninput = oninput
		self.pretext = pretext
		self.font = my.FONT(fontsize)
		self.box_image = pygame.transform.scale(box_image, self.size)
		self.text = ''

		self.timer = 0
		self.selected = False

	def update(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos in self:
				self.selected = True
			else:
				self.selected = False

		if self.selected:
			self.timer += 1
			if self.timer > 30:
				self.timer = 0

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_KP_ENTER or event.key == pygame.K_TAB:
					return None

				if event.key == 8 or event.key == pygame.K_DELETE:
					if len(self.text) > 0:
						self.text = self.text[0:len(self.text)-1]
				else:
					if len(self.text) > 16:
						return None

					self.text = self.text + event.unicode

				self.oninput(self.text)

	def render(self, screen):
		screen.blit(self.box_image, self.pos)

		if not self.selected and self.text == '':
			screen.blit(self.font.render(self.pretext, True, my.GREY), (self.pos[0]+self.size[0]//8, self.pos[1]+self.size[1]//4))
		elif len(self.text) > 0:
			textSurface = self.font.render(self.text, True, (0, 0, 0))
			screen.blit(textSurface, (self.pos[0]+self.size[0]//8, self.pos[1]+self.size[1]//4))
			if self.timer > 20:
				screen.blit(self.font.render('|', True, (0, 0, 0)),(self.pos[0] + self.size[0]//8 + textSurface.get_width() + 5, self.pos[1] + self.size[1] // 4))