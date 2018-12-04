import pygame, my, random, game, threading
from ui import ui, label
from time import sleep


class Wind:

	def __init__(self, game):
		self.wind = pygame.Vector2((0, 0))
		self.directionVector = pygame.Vector2((0.01, 0))

		self.startTimer = random.uniform(1, 2.55)
		self.timer = self.startTimer
		self.image = ui.IMAGES['arrow'].convert_alpha()
		self.arrow = label.Image([my.SCREEN_HALF_WIDTH, 40], self.image.copy())
		game.hud.addWidget(self.arrow)

		self.thread = threading.Thread(target=self.counter)
		self.thread.start()

	def cancel(self):
		self.thread.isAlive = False

	def counter(self):
		while self.thread.isAlive:
			sleep(0.5)
			self.timer -= 0.05
			if self.timer <= 0:
				self.change()
			else:
				self.update()

	def change(self):
		self.startTimer = random.uniform(1, 2.55)
		self.timer = self.startTimer
		self.wind = pygame.Vector2((0, 0))

		direction = bool(random.randrange(0, 1))
		oldVector = self.directionVector
		self.directionVector = pygame.Vector2((0.005 if direction else -0.005, 0))
		if oldVector != self.directionVector:
			self.image = pygame.transform.flip(self.image, True, False)

		self.wind += pygame.Vector2((0, 0))

	def update(self):
		self.wind += self.directionVector
		alpha = (self.startTimer - self.timer) * 100

		self.arrow.image = self.image.copy()
		self.arrow.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
