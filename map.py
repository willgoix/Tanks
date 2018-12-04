import pygame, my, random, math, lib.delayedfunc
import lib.opensimplex as opensimplex

FREQUENCY = 2  # 4 elevaçao/zoom, maior = menos distancia entre as ilhas
OCTAVES = 2  # 4 deixa menos redondo/suave
REDISTRIBUTION = 1  # 1


class Map(pygame.sprite.Sprite):

    def __init__(self, width, height, seed):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height

        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()

        self.blocks = [[my.BLOCK_NONE for y in range(self.height)] for x in range(self.width)]
        self.generator = opensimplex.OpenSimplex(seed)

    def geneate(self, game):
        for row in range(0, self.width):
            self.blocks.append([])
            for tile in range(0, self.height):
                noise = self.__generateNoise(row, tile, self.width, self.height)
                block = self.__getBlockByNoise(noise)

                self.image.set_at((row, tile), block)
                self.blocks[row].append(block)

    # self.image.set_alpha(150)

    def generate(self):
        for x in range(0, self.width):
            print(x)
            #my.ENGINE.game.hud.setStatus('Gerando mapa...', my.ENGINE.game.hud.bar.value + 1 / self.width)
            for y in range(0, 1):
                noise = self.__generateNoise(x, y, self.width, self.height)
                #print('x', x, '   y', y)

                self.square(x, y + int(noise * 200) - 100)

    def square(self, xx, y):
        for yy in range(self.height, self.height//2, -1):
            if xx >= self.width or xx < 0 or yy >= self.height or yy < 0:
                continue

            self.image.set_at((xx, yy), my.BLOCK_COLORS[my.BLOCK_ROCK])
            self.blocks[xx][yy] = my.BLOCK_ROCK

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect())

    def getMaxHeight(self, x):
        column = self.blocks[x]

        for y in range(self.height - 1, 0, -1):
            if column[y] == my.BLOCK_NONE:
                return y + 1

        return self.height

    def __getBlockByNoise(self, noise):
        if noise < 0:
            return my.BLOCK_ROCK
        elif noise < 0.2:
            return my.BLOCK_DIRT
        elif noise < 0.4:
            return my.BLOCK_GRASS
        else:
            return my.BLOCK_NONE

    def __noise(self, nx, ny):
        # Rescale from -1.0 : +1.0 to 0.0 : 1.0
        return self.generator.noise2d(nx, ny)  # / 2.0 + 0.5

    def __generateNoise(self, x, y, width, height):
        nx = x / width - 0.5
        ny = y / height - 0.5
        distance = 2 * max(abs(nx), abs(ny))
        result = 0

        freq = FREQUENCY
        for i in range(OCTAVES, 0, -1):
            # normal
            # nois += (i/octaves) * noise(nx*freq, ny*freq)

            # ilha - www.redblobgames.com/maps/terrain-from-noise/#islands
            a = 0.07
            b = 0.80
            c = 1.20

            noisTemp = (i / OCTAVES) * self.__noise(nx * freq, ny * freq)
            result += (noisTemp + a) * (1 - b * pow(distance, c))

            freq *= 2

        return pow(result, REDISTRIBUTION)
