class Widget:

	def __init__(self, pos, size):
		self.pos = pos
		self.size = size

	def __contains__(self, pos):
		return pos[0] > self.pos[0] and pos[0] < self.pos[0] + self.size[0] and pos[1] > self.pos[1] and pos[1] < self.pos[1] + self.size[1]

	def update(self, event):
		pass

	def render(self, screen):
		pass
