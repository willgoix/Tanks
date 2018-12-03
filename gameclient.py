import pygame, socket, select, random, time, packets


class GameClient:

    def __init__(self, player, serveraddress="127.0.0.1", serverport=9000):
        self.player = player

        self.clientport = random.randrange(0, 999) + 8000
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.connection.connect((serveraddress, serverport))
        # self.connection.bind((serveraddress, serverport))

        self.serveraddress = serveraddress
        self.serverport = serverport

        self.read_list = [self.connection]
        self.write_list = []

    def read(self):
        readable, writable, exceptional = (select.select(self.read_list, self.write_list, [], 0))

        for connection in readable:
            if connection is self.connection:
                data, address = connection.recvfrom(32)
                message = data.decode('unicode-escape')

                self.receive(packets.Packet.read(message))

    def receive(self, packet):
        player = self.player.game.getPlayer(packet.clientId)

        if isinstance(packet, packets.PacketSuccessConnect):
            packets.PacketConnect(self.clientport, self.serveraddress, self.clientport)

        elif isinstance(packet, packets.PacketConnect):
            self.player.game.entities.addPlayer()

        elif isinstance(packet, packets.PacketDisconnect):
            player.pos = (packet.x, packet.y)

        elif isinstance(packet, packets.PacketMovement):
            player.pos = (packet.x, packet.y)
