import pygame, my, game

PACKETS = {}

class Packet:

	""" ID | CLIENT_ID <-- Default structure  """
	def __init__(self, id, clientId, *args):
		self.id = id
		self.clientId = clientId
		self.args = args

		global PACKETS
		PACKETS[self.id] = self

	def constructData(self):
		return bytes(str(self.id) + '|'+ str(self.clientId) +'|'+ '|'.join(self.args), 'unicode-escape')

	@staticmethod
	def read(message):
		id = 0
		args = []
		for i in range(0, len(message.split('|'))):
			if i == 0:
				id = message.split('|')[i]
			else:
				args.append(message.split('|')[i])

		return PACKETS[id](args)

	def send(self):
		if my.ENGINE.game.online:
			my.ENGINE.game.getPlayer(self.clientId).client.connection.sendall(self.constructData()) # (self.client.address, self.client.serverport)


class PacketPreConnect(Packet):

	""" ID | CLIENT_ID | ADDRESS | PORT"""
	def __init__(self, clientId, address, port):
		Packet.__init__(self, 1, clientId, '|'.join(address, port))
		self.address = address
		self.port = port

class PacketConnectSuccess(Packet): # SERVER PACKET

	""" ID | CLIENT_ID | ADDRESS | PORT"""
	def __init__(self, clientId, address, port):
		Packet.__init__(self, 2, clientId, '|'.join(address, port))
		self.address = address
		self.port = port


class PacketConnectRefused(Packet): # SERVER PACKET

	""" ID | CLIENT_ID | ADDRESS | PORT"""
	def __init__(self, clientId, address, port, reason):
		Packet.__init__(self, 3, clientId, '|'.join(address, port, reason))
		self.address = address
		self.port = port
		self.reason = reason


class PacketConnect(Packet):

	""" ID | CLIENT_ID | ADDRESS | PORT """
	def __init__(self, clientId, address, port):
		Packet.__init__(self, 3, clientId, '|'.join(address, port))
		self.address = address
		self.port = port


class PacketDisconnect(Packet):

	""" ID | CLIENT_ID """
	def __init__(self, clientId, reason):
		Packet.__init__(self, 4, clientId, '|'.join(reason))
		self.reason = reason


class PacketMap(Packet):

	""" ID | CLIENT_ID | WIDTH | HEIGHT | SEED """
	def __init__(self, clientId, width, height, seed):
		Packet.__init__(self, 5, clientId, '|'.join(width, height, seed))
		self.height = height
		self.width = width
		self.seed = seed


class PacketSpawnPlayer(Packet):

	""" ID | CLIENT_ID | X | Y """
	def __init__(self, clientId, x, y):
		Packet.__init__(self, 6, clientId, '|'.join(x, y))
		self.x = x
		self.y = y


class PacketSpawnEnemy(Packet):

	""" ID | CLIENT_ID | X | Y """
	def __init__(self, clientId, x, y):
		Packet.__init__(self, 7, clientId, '|'.join(x, y))
		self.x = x
		self.y = y


class PacketMovement(Packet):

	""" ID | CLIENT_ID | X | Y """
	def __init__(self, clientId, x, y):
		Packet.__init__(self, 8, clientId, '|'.join([str(x), str(y)]))
		self.x = x
		self.y = y


class PacketLaunch(Packet):

	""" ID | CLIENT_ID | X | Y | VELOCITYX | VELOCITYY | IS_ENEMY  """
	def __init__(self, clientId, x, y, velocityx, velocityy, enemy):
		Packet.__init__(self, 9, clientId, '|'.join(x, y, velocityx, velocityy, enemy))
		self.x = x
		self.y = y
		self.velocityx = velocityx
		self.velocityy = velocityy
		self.enemy = enemy









