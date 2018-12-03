import pygame, my, entities, ui, sound, random, lib.delayedfunc, threading
from time import sleep
from ui import label


class TurnController:

	def __init__(self, game):
		self.game = game

		self.timer = 25
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
		self.doStartAnimation()
		self.thread.start()

	def next(self):
		lives = self.game.getLiveEntities()

		if self.currentIndex < len(lives) - 1:
			if self.currentEntity is not None: self.currentEntity.onEndTurn()
			self.currentEntity = lives[self.currentIndex]
			self.timer = 25
			self.currentIndex += 1

			self.doTurnAnimation()
			self.game.entities.setTarget(self.currentEntity)

			if isinstance(self.currentEntity, entities.Player):
				self.doPlayerTurn(self.currentEntity)
			else:
				self.doAITurn(self.currentEntity)
		else:
			self.currentIndex = 0
			self.next()

	def doPlayerTurn(self, entity):
		sound.play('kill_' + str(random.randint(1, 3)))

	def doAITurn(self, entity):
		pass

	def doStartAnimation(self):
		def animation():
			counter = ui.label.Text(my.SCREEN_HALF_SIZE, '5', fontsize=30)
			self.game.hud.addWidget(counter)

			for i in range(0, -1, -1):
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

	def doTurnAnimation(self):
		text = label.Text(my.SCREEN_HALF_SIZE,
						  'Seu turno é agora!' if self.currentEntity == self.game.player else 'Turno de: '+ self.currentEntity.nickname,
						  fontsize=30)
		self.game.hud.addWidget(text)

		def removeWidget():
			self.game.hud.removeWidget(text)

		lib.delayedfunc.DelayedFunc(lambda: removeWidget(), 3)