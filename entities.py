import pygame, my, gameclient, random, packets, math, sound


class Entity(pygame.sprite.Sprite):

	def __init__(self, game, id, nickname, tank, pos):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.id = id
		self.nickname = nickname
		self.tank = tank

		self.image = tank.image.copy()
		self.rect = self.image.get_rect(bottom=pos[1])
		self.rect.x = pos[0]
		self.rect.y = pos[1]

		self.pos = [pos[0], pos[1]]
		self.velocity = pygame.Vector2((0, 0)) #my.GRAVITY
		self.onGround = False
		self.speed = tank.speed
		self.health = tank.health
		self.fuel = tank.fuel

		self.flipped = False

	def checkDie(self):
		if self.health <= 0:
			print(self, ' killed')
			#Packet
			self.game.hud.removeWidgets(self)

			self.kill()
			self.game.checkWinner()
			return True
		return False

	def collide(self, xvelocity, yvelocity):
		size = self.rect.w
		half_tank = self.rect.h/2


		for blockx in range(self.rect.x - size, self.rect.x + size):
			for blocky in range(self.rect.y+70, self.rect.y+60, -1):
			#for blocky in range(self.rect.centery+self.rect.h//2, self.rect.centery, -1):
				if blockx < len(self.game.map.blocks) and blocky < len(self.game.map.blocks[blockx]):
					block = self.game.map.blocks[blockx][blocky]

					if block == my.BLOCK_NONE:
						continue

					if blockx > self.rect.x and blockx < self.rect.x + self.rect.w and blocky > self.rect.y and blocky < self.rect.y + self.rect.h:
						if xvelocity > 0:
							maxy = self.game.map.getMaxHeight(blockx)
							if (blocky - half_tank) < maxy:
								self.rect.bottom = maxy
							self.rect.right = blockx
						if xvelocity < 0:
							maxy = self.game.map.getMaxHeight(blockx)
							if (blocky - half_tank) < maxy:
								self.rect.bottom = maxy
							self.rect.left = blockx
						if yvelocity > 0:
							self.rect.bottom = blocky
							self.onGround = True
							self.velocity.y = 0
						if yvelocity < 0:
							self.rect.top = blocky


class Player(Entity):

	def __init__(self, game, nickname, tank, pos):
		Entity.__init__(self, game, 0, nickname, tank, pos)
		self.client = gameclient.GameClient(self)
		self.id = self.client.clientport

		self.fuel = 10000 ################################################################################ remover

	def update(self):
		oldx, oldy = self.rect.x, self.rect.y

		if self.game.turncontroller.check(self):
			self.move()

		# Move by gravity
		if not self.onGround:
			self.velocity += my.GRAVITY
			if self.velocity.y > 100: self.velocity.y = 100

		self.rect.top += self.velocity.y
		self.onGround = False
		self.collide(0, self.velocity.y)

		self.pos = [self.rect.x, self.rect.y]
		self.updateRotation()

		if self.rect.x != oldx or self.rect.y != oldy:
			packets.PacketMovement(self.id, self.rect.x, self.rect.y).send()



		if Entity.checkDie(self):
			sound.play('game_over')

	def move(self):
		pressed = pygame.key.get_pressed()
		left = pressed[pygame.K_LEFT]
		right = pressed[pygame.K_RIGHT]

		if left or right:
			self.fuel -= 1
			if self.fuel <= 0:
				return None

		if left:
			self.velocity.x = -self.speed
		if right:
			self.velocity.x = self.speed
		if not (left or right):
			self.velocity.x = 0

		self.rect.left += self.velocity.x
		self.collide(self.velocity.x, 0)

	def updateRotation(self):
		x, y = pygame.mouse.get_pos()
		if x > self.rect.x and self.flipped:
			self.flipped = False
			self.image = pygame.transform.flip(self.image, True, False)
		if x < self.rect.x and not self.flipped:
			self.flipped = True
			self.image = pygame.transform.flip(self.image, True, False)


class Enemy(Entity):

	def __init__(self, game, tank, pos):
		Entity.__init__(self, game, random.randint(0, 1000), my.NAMES[random.randint(0, len(my.NAMES))-1], tank, pos)

	def update(self):
		oldx, oldy = self.rect.x, self.rect.y

		if self.game.turncontroller.check(self):
			self.move(self.findWaypoint())

		if not self.onGround:
			self.velocity += my.GRAVITY
			if self.velocity.y > 100: self.velocity.y = 100

		self.rect.top += self.velocity.y
		self.onGround = False
		self.collide(0, self.velocity.y)
		self.pos = [self.rect.x, self.rect.y]

		if self.rect.x != oldx or self.rect.y != oldy:
			packets.PacketMovement(self.id, self.rect.x, self.rect.y).send()



		Entity.checkDie(self)

	def move(self, waypoint):
		left = not waypoint[0]
		right = waypoint[0]

		if left or right:
			self.fuel -= 1
			if self.fuel <= 0:
				return None

		if waypoint[1] <= 20:
			left, right = right, left

		if left:
			self.velocity.x = -self.speed
		if right:
			self.velocity.x = self.speed
		if not (left or right):
			self.velocity.x = 0

		self.rect.left += self.velocity.x
		self.collide(self.velocity.x, 0)

	def findWaypoint(self):
		nearestx = self.game.width
		for entity in self.game.getLiveEntities():
			if math.fabs(entity.pos[0] - self.pos[0]) < nearestx:
				nearestx = entity.pos[0] - self.pos[0]

		return (False, math.fabs(nearestx)) if nearestx < 0 else (True, math.fabs(nearestx)) #direita = true	esquerda = false
