import pygame, my, entities, threading, ui, sound
from time import sleep


class TurnController:

	def __init__(self, game):
		self.game = game

		self.timer = 60
		self.currentEntity = None
		self.currentIndex = -1

		self.thread = threading.Thread(target=self.counter)

	def check(self, entity):
		return self.currentEntity == entity

	def counter(self):
		while self.thread.isAlive:
			sleep(1)
			self.timer -= 1

			if self.timer <= 0:
				self.next()

	def start(self):
		self.doAnimation()
		self.thread.start()

	def next(self):
		lives = self.game.getLiveEntities()

		if self.currentIndex < len(lives) - 1:
			self.currentEntity = lives[self.currentIndex]
			self.timer = 60
			self.currentIndex += 1

			if isinstance(self.currentEntity, entities.Player):
				self.doPlayerTurn(self.currentEntity)
			else:
				self.doAITurn(self.currentEntity)
		else:
			self.currentIndex = 0
			self.next()

	def doPlayerTurn(self, entity):
		self.game.entities.setTarget(entity)

	def doAITurn(self, entity):
		pass

	def doAnimation(self):
		def animation():
			counter = ui.label.Text(my.SCREEN_HALF_SIZE, '5', fontsize=30)
			self.game.hud.addWidget(counter)

			for i in range(5, -1, -1):
				if i == 0:
					sound.play('fight')
					counter.pos[0] -= 60
					counter.text = 'COMEÇOU'
				else:
					sound.play(str(i))
					counter.text = str(i)
				sleep(1)

			self.game.hud.removeWidget(counter)
			self.next()

		threadAnimation = threading.Thread(target=animation)
		threadAnimation.start()