import pygame

pygame.init()

import socket
import select
import random
import time

"""
movimentos do tanque
movimentos do canhão
disparo
"""


class GameClient(object):

	def __init__(self, address="127.0.0.1", serverport=9009):
		self.clientport = random.randrange(8000, 8999)
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.connection.bind(("127.0.0.1", self.clientport))
		self.address = address
		self.serverport = serverport

		self.read_list = [self.connection]
		self.write_list = []

	def read(self):
		readable, writable, exceptional = (
			select.select(self.read_list, self.write_list, [], 0)
		)

		for read in readable:
			if read is self.connection:
				data, addr = read.recvfrom(32)
				msg = data.decode('unicode-escape')

				self.screen.blit(self.bg_surface, (0, 0))  # Draw the background

				for position in msg.split('|'):
					x, sep, y = position.partition(',')
					try:
						self.screen.blit(self.image, (int(x), int(y)))
					except:
						print("!!!!!!!! erro ao desenhar")

	def write(self):
		pressed = pygame.key.get_pressed()
		up = pressed[pygame.K_UP]
		left = pressed[pygame.K_LEFT]
		right = pressed[pygame.K_RIGHT]
		running = pressed[pygame.K_SPACE]

		if up:
			self.connection.sendto(bytes("up", 'unicode-escape'), (self.address, self.serverport))