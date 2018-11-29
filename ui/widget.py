from .ui import CENTER, UPPER, BOTTOM, LEFT, RIGHT


class Widget:

	def __init__(self, pos, size, centralization=CENTER):
		self.pos = [pos[0], pos[1]]  #Para não modificar variáveis estáticas
		self.size = [size[0], size[1]]

		if BOTTOM & centralization == BOTTOM:
			self.pos[1] += size[1] / 2
		if UPPER & centralization == UPPER:
			self.pos[1] -= size[1] / 2
		if LEFT & centralization == LEFT:
			self.pos[0] -= size[0] / 2
		if RIGHT & centralization == RIGHT:
			self.pos[0] += size[0] / 2
		if CENTER & centralization == CENTER or centralization == 0:
			self.pos[0] -= size[0] / 2
			self.pos[1] -= size[1] / 2

	def __contains__(self, pos):
		return pos[0] > self.pos[0] and pos[0] < self.pos[0] + self.size[0] and pos[1] > self.pos[1] and pos[1] < self.pos[1] + self.size[1]

	def update(self, event):
		pass

	def render(self, screen):
		pass
