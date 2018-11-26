import pygame
from my import PLATFORM_WIDTH, PLATFORM_HEIGHT, RED, BLUE, DARK_GREEN, GRAVITY
import game

AIR = 0
GRASS = 1
DIRT = 2
STONE = 3

NAMES = {
	AIR: "Air",
	GRASS: "Grass",
	DIRT: "Dirt",
	STONE: "Stone"
}

SOLID = {
	AIR: False,
	GRASS: True,
	DIRT: True,
	STONE: True
}

IMAGES = {
	AIR: None,
	GRASS: pygame.image.load("assets/platforms/grass.png").convert(),
	DIRT: pygame.image.load("assets/platforms/dirt.png").convert(),
	STONE: pygame.image.load("assets/platforms/stone.png").convert()
}


class Entity(pygame.sprite.Sprite):
	def __init__(self, screenx, screeny):
		pygame.sprite.Sprite.__init__(self)
		self.screenx = screenx
		self.screeny = screeny
		self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.rect = self.image.get_rect(topleft=(screenx, screeny))


class Player(Entity):
	def __init__(self, game, screenx, screeny):
		Entity.__init__(self, screenx, screeny)
		self.game = game
		#TODO: Melhorar definição de imagens/rect
		image = pygame.image.load("assets/backgrounds/cloud_1.png")
		self.image = image
		self.rect = self.image.get_rect(topleft=(screenx, screeny))

		self.velocity = pygame.Vector2((0, 0))
		self.onGround = False
		self.speed = 8
		self.jump_strength = 5

	def update(self):
		pressed = pygame.key.get_pressed()
		up = pressed[pygame.K_UP]
		left = pressed[pygame.K_LEFT]
		right = pressed[pygame.K_RIGHT]
		running = pressed[pygame.K_SPACE]

		if up:
			# only jump if on the ground
			if self.onGround:
				self.velocity.y = -self.jump_strength
		if left:
			self.velocity.x = -self.speed
		if right:
			self.velocity.x = self.speed
		if running:
			self.velocity.x *= 1.5
		if not self.onGround:
			# only accelerate with gravity if in the air
			self.velocity += GRAVITY
			# max falling speed
			if self.velocity.y > 100: self.velocity.y = 100

		if not (left or right):
			self.velocity.x = 0

		# increment in x direction
		self.rect.left += self.velocity.x
		# do x-axis collisions
		self.collide(self.velocity.x, 0)

		# increment in y direction
		self.rect.top += self.velocity.y
		# assuming we're in the air
		self.onGround = False
		# do y-axis collisions
		self.collide(0, self.velocity.y)

	def collide(self, xvelocity, yvelocity):
		#TODO: Ver a possibilidade de pegar apenas as plataformas por perto (seria necessário transformar o Group platforms em uma lista)
		for plat in self.game.map.platforms:
			if pygame.sprite.collide_rect(self, plat):
				# if isinstance(p, ExitBlock):
				#	pygame.event.post(pygame.event.Event(QUIT))
				if xvelocity > 0:
					self.rect.right = plat.rect.left
				if xvelocity < 0:
					self.rect.left = plat.rect.right
				if yvelocity > 0:
					self.rect.bottom = plat.rect.top
					self.onGround = True
					self.velocity.y = 0
				if yvelocity < 0:
					self.rect.top = plat.rect.bottom


class Platform(Entity):

	def __init__(self, ID, screenx, screeny, cartx, carty):
		Entity.__init__(self, screenx, screeny)

		self.cartx = cartx
		self.carty = carty

		self.ID = ID
		self.image.set_alpha(0)

		if IMAGES[ID] is not None: self.image = pygame.transform.scale(IMAGES[ID], (PLATFORM_WIDTH, PLATFORM_HEIGHT))
