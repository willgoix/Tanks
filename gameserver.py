import socket, select, sys, threading, packets
from time import sleep


class GameServer:

	def __init__(self, address='192.168.0.9', port=9000, max_players=2):
		self.address = address
		self.port = port
		self.max_players = max_players

		self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.listener.bind((address, port))
		self.read_list = [self.listener]
		self.write_list = []

		self.players = []
		self.thread = None

	def start(self):
		print("Iniciando servidor...")
		print("Endereço: {}        Porta: {}{}".format(self.address, self.port, '\n\n'))

		self.thread = threading.Thread(target=self.run)
		self.thread.start()

	def run(self):
		try:
			while True:
				readable, writable, exceptional = ( select.select(self.read_list, self.write_list, []) )

				for connection in readable:
					if connection is self.listener:
						data, address = connection.recvfrom(32)
						message = data.decode("unicode-escape")

						packet = packets.Packet.read(message)
						self.receive(packet)
		except Exception as e:
			print("[ERRO]: ", e)
			sleep(1000)

	def receive(self, packet):
		#player = self.game.getPlayer(packet.clientId)
		print("[RECEIVED PACKET] "+ str(packet.clientId) +" > ("+ str(packet.id) +")"+ packet.args)

		if isinstance(packet, packets.PacketPreConnect):
			if len(self.players) >= self.max_players:
				self.send(packets.PacketDisconnect(packet.clientId, 'Servidor cheio'), (packet.address, packet.port))
				return
			for player in self.players:
				if player == packets.clientId:
					self.send(packets.PacketDisconnect(packet.clientId, 'IDs iguais, tente novamente'), (packet.address, packet.port))
					return
			packets.PacketSuccessConnect(packet.clientId, packet.address, packet.port).send()

		elif isinstance(packet, packets.PacketConnect):
			self.players.append[packet.clientId] = (packet.address, packet.port)

		elif isinstance(packet, packets.PacketDisconnect):
			del self.players[packet.clientId]

		self.send(packet)

	def send(self, packet, address=None):
		print("[SEND PACKET] " + str(packet.clientId) + " > (" + str(packet.id) + ")" + packet.args)

		if address is None:
			for player in self.players:
				self.listener.sendto(packet.constructData(), self.players[player])
		else:
			self.listener.sendto(packet.constructData(), address)