import pygame
from .ui import CENTER
from .widget import Widget
from my import BLACK, FONT

CURSOR_NORMAL = pygame.cursors.arrow
CURSOR_HOVERED = pygame.cursors.broken_x
CURSOR_CLICKED = pygame.cursors.diamond


class Button(Widget):
	def __init__(self, onclick, pos, size, centralization=CENTER):
		Widget.__init__(self, pos, size)
		self.onclick = onclick
		self.centralization = centralization
		self.surface = pygame.Surface(size)
		self.clicked = False
		self.hovered = False

	def asRect(self):
		return pygame.Rect(self.pos, self.size)

	def setText(self, text):
		self.text = text

	def click(self):
		if self.clicked: return False

		self.clicked = True
		self.onclick()

	def unclick(self):
		if not self.clicked: return False

		self.clicked = False

	def update(self, event):
		if event.type == pygame.MOUSEMOTION:
			if self.clicked:
				pygame.mouse.set_cursor(*CURSOR_CLICKED)
			elif self.hovered:
				pygame.mouse.set_cursor(*CURSOR_HOVERED)
			else:
				pygame.mouse.set_cursor(*CURSOR_NORMAL)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if self.clicked:
				pygame.mouse.set_cursor(*CURSOR_CLICKED)
		elif event.type == pygame.MOUSEBUTTONUP:
			if not self.clicked and self.hovered:
				pygame.mouse.set_cursor(*CURSOR_HOVERED)


class TextButton(Button):
	def __init__(self, onclick, pos, size, text="", color=BLACK, centralization=CENTER):
		Button.__init__(self, onclick, pos, size, centralization)

		self.text = text
		self.color = color
		self.color_pressed = self._get_darker_color(80)
		self.color_hovered = self._get_darker_color(20)

	def _get_darker_color(self, percentage):
		""" Retorna uma cor X% mais escura """

		r, g, b, *_ = tuple(self.color)
		const = percentage / 100
		r = int(const * r)
		g = int(const * g)
		b = int(const * b)

		return (r, g, b)

	def update(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos in self:
				self.click()

		elif event.type == pygame.MOUSEBUTTONUP:
			self.unclick()

		elif event.type == pygame.MOUSEMOTION:
			if event.pos in self:
				self.hovered = True
			else:
				self.hovered = False

		Button.update(self, event)

	def render(self, screen):
		if self.clicked:
			color = self.color_pressed
		elif self.hovered:
			color = self.color_hovered
		else:
			color = self.color

		self.surface.fill(color)
		screen.blit(self.surface, self.pos)

		fontSurface = FONT(12).render(self.text, True, [0, 0, 0])
		centralizedX = self.pos[0] + self.surface.get_width() / 2 - fontSurface.get_width() / 2
		centralizedY = self.pos[1] + self.surface.get_height() / 2 - fontSurface.get_height() / 2

		screen.blit(fontSurface, (centralizedX, centralizedY))


class ImageButton(Button):
	def __init__(self, onclick, pos, text, size=[0, 0], image_surface=None, image_pressed=None, image_hovered=None, centralization=CENTER):
		Button.__init__(self, onclick, pos, size)

		self.text = text
		self.image = pygame.transform.smoothscale(image_surface, self.size)

		if image_pressed is None:
			self.image_pressed = self._get_darker_image(80)
		else:
			self.image_pressed = pygame.transform.smoothscale(image_pressed, self.size)

		if image_hovered is None:
			self.image_hovered = self._get_darker_image(20)
		else:
			self.image_hovered = pygame.transform.smoothscale(image_hovered, self.size)

	def _get_darker_image(self, percentage):
		""" Retorna uma imagem X% mais escura """
		image_dark = self.image.copy()

		for x in range(self.size[0]):
			for y in range(self.size[1]):
				r, g, b, *_ = tuple(self.image.get_at((x, y)))
				const = (100 - percentage) / 100
				r = int(const * r)
				g = int(const * g)
				b = int(const * b)
				image_dark.set_at((x, y), (r, g, b))

		return image_dark

	def update(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos in self:
				self.click()

		elif event.type == pygame.MOUSEBUTTONUP:
			self.unclick()

		elif event.type == pygame.MOUSEMOTION:
			if event.pos in self:
				self.hovered = True
			else:
				self.hovered = False

		Button.update(self, event)

	def render(self, screen):
		if self.clicked:
			image = self.image_pressed
		elif self.hovered:
			image = self.image_hovered
		else:
			image = self.image

		screen.blit(image, self.pos)

		fontSurface = FONT(30).render(self.text, True, [0, 0, 0])
		centralizedX = self.pos[0] + image.get_width() / 2 - fontSurface.get_width() / 2
		centralizedY = self.pos[1] + image.get_height() / 2 - fontSurface.get_height() / 2

		screen.blit(fontSurface, (centralizedX, centralizedY))
