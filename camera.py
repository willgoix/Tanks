import pygame
from my import SCREEN_WIDTH, SCREEN_HEIGHT

SCREEN_WIDTH_HALF = SCREEN_WIDTH / 2
SCREEN_HEIGHT_HALF = SCREEN_HEIGHT / 2


class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):

	def __init__(self, target, world_size):
		pygame.sprite.LayeredUpdates.__init__(self)
		self.cam = pygame.Vector2(0, 0)
		self.world_size = world_size
		self.spritedict = {}

		self.setTarget(target)

	def setTarget(self, target):
		self.target = target
		if self.target: self.add(target)

	def update(self, *args):
		super().update(*args)
		if self.target:
			x = -self.target.rect.center[0] + SCREEN_WIDTH_HALF
			y = -self.target.rect.center[1] + SCREEN_HEIGHT_HALF
			self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
			self.cam.x = max(-(self.world_size.width - SCREEN_WIDTH), min(0, self.cam.x))
			self.cam.y = max(-(self.world_size.height - SCREEN_HEIGHT), min(0, self.cam.y))

	def draw(self, surface):
		spritedict = self.spritedict
		surface_blit = surface.blit
		dirty = self.lostsprites
		self.lostsprites = []
		dirty_append = dirty.append
		init_rect = self._init_rect
		for spr in self.sprites():
			rec = spritedict[spr]
			newrect = surface_blit(spr.image, spr.rect.move(self.cam))
			if rec is init_rect:
				dirty_append(newrect)
			else:
				if newrect.colliderect(rec):
					dirty_append(newrect.union(rec))
				else:
					dirty_append(newrect)
					dirty_append(rec)
			spritedict[spr] = newrect
		return dirty