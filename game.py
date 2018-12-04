import pygame, map, my, entities, camera, hud, loading, tank, gameserver, turn, sound, menu, wind, lib.delayedfunc, ui.label
from random import randint
from functools import partial


class Game:
	"""
	gameConfigurations[1] = enemiesCount

	playerConfigurations[0] = nickname

	mapConfigurations[0] = width
	mapConfigurations[1] = height
	mapConfigurations[3] = seed
	"""

	def __init__(self, online, gameConfigurations=[], playerConfigurations=[], mapConfigurations=[]):
		self.online = online
		self.enemiesCount = gameConfigurations[0]

		self.playerConfigurations = playerConfigurations

		self.width = mapConfigurations[0]
		self.height = mapConfigurations[1]
		self.seed = mapConfigurations[2]

		self.player = None
		self.entities = None
		self.map = None
		self.hud = None
		self.turncontroller = None
		self.wind = None
		self.running = False

	def start(self):
		self.hud = loading.Loading(my.ENGINE.screen)

		self.map = map.Map(self.width, self.height, self.seed)
		self.map.generate()

		self.hud.setStatus('Carregando entidades...', 80)
		self.player = entities.Player(self, self.playerConfigurations[0], tank.TankDefault(), (100, 100))
		self.entities = camera.CameraAwareLayeredUpdates(self.player, pygame.Rect(0, 0, self.width, self.height))
		self.entities.add(self.map)  # Adicionando o mapa em entidades para poder ser scrollado
		for i in range(0, self.enemiesCount):
			x = randint(50, self.width - 50)
			self.entities.add(entities.Enemy(self, tank.TankDefault(), (x, self.map.getMaxHeight(x))))

		self.hud.setStatus('Carregando interface...', 99)
		self.hud = hud.Hud(self, my.ENGINE.screen)
		my.ENGINE.interface = self.hud
		self.turncontroller = turn.TurnController(self)
		self.turncontroller.start()

		self.wind = wind.Wind(self)

		self.running = True

	def tick(self):
		if self.running:
			my.ENGINE.screen.fill(my.LIGHT_BLUE)

			#TODO: Remover isso
			for e in my.ENGINE.event_manager.events:
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_t:
						self.turncontroller.next()

					if e.key == pygame.K_m:
						self.player.health = 0

					if e.key == pygame.K_f:
						self.player.fuel = 100

			""" ATUALIZANDO """
			self.entities.update()

			""" DESENHANDO """
			#self.map.draw(my.ENGINE.screen)
			self.entities.draw(my.ENGINE.screen)

	def end(self):
		lib.delayedfunc.cancelAll()
		self.turncontroller.cancel()
		self.wind.cancel()
		self.running = False

		#self.entities.empty()
		#self.__dict__.clear()
		self.hud.next = menu.Menu(my.ENGINE.screen)
		my.ENGINE.game = None

	def checkWinner(self):
		lives = self.getLiveEntities()

		if len(lives) == 1:
			winner = lives[0]

			if winner == self.player:
				sound.play('you_win')
				self.hud.addWidget(ui.label.Text(my.SCREEN_HALF_SIZE, "Você venceu!", fontsize=40))

				self.turncontroller.cancel()
				lib.delayedfunc.DelayedFunc(partial(self.end), 3)
		elif len(lives) == 0:
			self.hud.addWidget(ui.label.Text(my.SCREEN_HALF_SIZE, "Ninguém venceu!", fontsize=40))

			self.turncontroller.cancel()
			lib.delayedfunc.DelayedFunc(partial(self.end), 3)


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

	def __init__(self, gameConfigurations=[], playerConfigurations=[], mapConfigurations=[]):
		Game.__init__(self, False, gameConfigurations, playerConfigurations, mapConfigurations)


class GameOnline(Game):

	def __init__(self, isServer, gameConfigurations=[], playerConfigurations=[], mapConfigurations=[]):
		Game.__init__(self, True, gameConfigurations, playerConfigurations, mapConfigurations)
		self.isServer = isServer
		self.server = gameserver.GameServer('localhost')
