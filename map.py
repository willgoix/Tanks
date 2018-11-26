from my import SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT
import pygame
import sprites
import random
import lib.opensimplex as opensimplex


class Map:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.platforms = pygame.sprite.Group()

    def generate(self, game):
        for row in range(0, self.width):
            for tile in range(0, self.height):
                cartx = tile * PLATFORM_WIDTH  # CARTESIANO
                carty = row * PLATFORM_HEIGHT

                noise = genNoise(row, tile, self.width, self.height)
                pos = cartx, carty  # y if noise < 0 else y-noise*BLOCK_SIZE_PIXELS)
                platform = self.__getPlatformByNoise(cartx, carty, tile, row, noise)

                if platform is not None:
                    game.entities.add(platform)
                    self.platforms.add(platform)

    def draw(self, screen):
        for row in range(0, self.width):
            for tile in range(0, self.height):
                platform = self.getPlatform(row, tile)
                platform.draw(screen)

    def getPlatform(self, cartx, carty):
        for plat in self.platforms:
            if plat.cartx == cartx and plat.carty == carty:
                return plat

    def __getPlatformByNoise(self, screenx, screeny, cartx, carty, noise):
        if noise < 0:
            return None#sprites.Platform(sprites.AIR, screenx, screeny, cartx, carty)
        elif noise < 0.1:
            return sprites.Platform(sprites.GRASS, screenx, screeny, cartx, carty)
        elif noise < 0.2:
            return sprites.Platform(sprites.DIRT, screenx, screeny, cartx, carty)
        else:
            return sprites.Platform(sprites.STONE, screenx, screeny, cartx, carty)


gen = opensimplex.OpenSimplex(seed=random.randint(0, 10000))
frequency = 4  # 4 elevação/zoom, maior = menos distância entre as ilhas
octaves = 2  # 4 deixa menos redondo/suave
redistribution = 1  # 1


def noise(nx, ny):
    # Rescale from -1.0 : +1.0 to 0.0 : 1.0
    return gen.noise2d(nx, ny)  # / 2.0 + 0.5


def genNoise(x, y, width, height):
    nx = x / width - 0.5
    ny = y / height - 0.5
    distance = 2 * max(abs(nx), abs(ny))
    result = 0

    freq = frequency
    for i in range(octaves, 0, -1):
        # normal
        # nois += (i/octaves) * noise(nx*freq, ny*freq)

        # ilha - www.redblobgames.com/maps/terrain-from-noise/#islands
        a = 0.07
        b = 0.80
        c = 1.20

        noisTemp = (i / octaves) * noise(nx * freq, ny * freq)
        result += (noisTemp + a) * (1 - b * pow(distance, c))

        freq *= 2

    return pow(result, redistribution)
