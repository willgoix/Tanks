import pygame, map, my, entities, camera, hud, loading, tank, bullet, gameserver, turn, sound
from random import randint


class Game:

	def __init__(self, online, width, height, seed, enemiesCount):
		self.online = online
		self.width = width
		self.height = height
		self.seed = seed
		self.enemiesCount = enemiesCount

		self.player = None
		self.entities = None
		self.map = None
		self.hud = None
		self.turncontroller = None
		self.running = False

	def start(self):
		self.hud = loading.Loading(my.ENGINE.screen)

		#self.hud.setStatus('Gerando mapa...', 20)
		self.map = map.Map(self.width, self.height, self.seed)
		self.map.generate()

		self.hud.setStatus('Carregando entidades...', 80)
		self.player = entities.Player(self, 'Tester', tank.TankDefault(), (100, 100))
		self.entities = camera.CameraAwareLayeredUpdates(self.player, pygame.Rect(0, 0, self.width, self.height))
		self.entities.add(self.map) #Adicionando o mapa em entidades para poder ser scrollado
		for i in range(0, self.enemiesCount):
			x = randint(50, self.width-50)
			self.entities.add(entities.Enemy(self, tank.TankDefault(), (x, self.map.getMaxHeight(x))))

		self.hud.setStatus('Carregando interface...', 99)
		self.hud = hud.Hud(self, my.ENGINE.screen)
		my.ENGINE.interface = self.hud
		self.turncontroller = turn.TurnController(self)
		self.turncontroller.start()

		self.running = True

	def tick(self):
		if self.running:
			for e in my.ENGINE.event_manager.events:
				if e.type == pygame.KEYDOWN and e.key == pygame.K_t:
					self.turncontroller.next()

			""" ATUALIZANDO """
			self.entities.update()

			""" DESENHANDO """
			self.entities.draw(my.ENGINE.screen)

	def checkWinner(self):
		lives = self.getLiveEntities()

		if len(lives) == 1:
			winner = lives[0]

			if winner == self.player:
				sound.play('you_win')


	def getLiveEntities(self):
		list = []
		for entity in self.entities:
			if isinstance(entity, entities.Player) or isinstance(entity, entities.Enemy):
				list.append(entity)
		return list

	def getPlayers(self):
		players = []
		for entity in self.entities:
			if isinstance(entity, entities.Player):
				players.append(entity)
		return players

	def getPlayer(self, id):
		for entity in self.entities:
			if isinstance(entity, entities.Player):
				if entity.id == id:
					return entity


class GameOffline(Game):

	def __init__(self, width, height, seed, enemiesCount):
		Game.__init__(self, False, width, height, seed, enemiesCount)


class GameOnline(Game):

	def __init__(self, width, height, seed, enemiesCount, isServer):
		Game.__init__(self, True, width, height, seed, enemiesCount)
		self.isServer = isServer
		self.server = gameserver.GameServer('localhost')
