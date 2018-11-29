import pygame, sprites, map, my
from camera import CameraAwareLayeredUpdates
from random import randint
from math import cos, sin
from menu import Menu


# https://github.com/jmoenig/morphic.py/blob/master/morphic.py

class Game:
    def __init__(self):
        self.screen = None
        self.player = None
        self.map = None
        self.entities = None

        self.background = None

        self.running = True
        self.menu = None

    # self.window = MenuWindow()

    def init(self):
        # TODO: Remover isso daqui, e fazer com que o preto das partes transparentes ao usar .convert() não apareça.
        for img in sprites.IMAGES:
            if sprites.IMAGES[img] is not None:
                sprites.IMAGES[img].set_colorkey((0, 0, 0))
                sprites.IMAGES[img].set_colorkey((255, 0, 255))

        self.background = pygame.image.load("assets/backgrounds/top_" + str(randint(1, 1)) + ".png")
        self.background.blit(pygame.image.load("assets/backgrounds/bottom_" + str(randint(1, 3)) + ".png"), (0, 0))
        self.background = pygame.transform.scale(self.background, (my.SCREEN_WIDTH, my.SCREEN_HEIGHT))

        self.screen = pygame.display.set_mode((my.SCREEN_WIDTH, my.SCREEN_HEIGHT))
        pygame.display.set_caption("Minhoquinhas - v", my.VERSION)

        total_width = 100 * my.PLATFORM_WIDTH
        total_height = 100 * my.PLATFORM_HEIGHT
        self.player = sprites.Player(self, my.PLATFORM_WIDTH, my.PLATFORM_HEIGHT)
        self.entities = CameraAwareLayeredUpdates(self.player, pygame.Rect(20, 20, total_width, total_height))

        self.map = map.Map(100, 100)
        self.map.generate(self)

        self.menu = Menu(self.screen)

    def loop(self):
        self.eventsTick = pygame.event.get()
        for event in self.eventsTick:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # playerNew = sprites.Player(self, PLATFORM_WIDTH, PLATFORM_HEIGHT)
                # self.entities.setTarget(playerNew)

                mapx = self.player.rect.x // my.PLATFORM_WIDTH
                mapy = self.player.rect.y // my.PLATFORM_HEIGHT

                circle = pygame.draw.circle(self.screen, (255, 0, 255), (self.player.rect.x, self.player.rect.y), 20)
                for x in range(mapx - 5, mapx + 5):
                    for y in range(mapy - 5, mapy + 5):
                        platform = self.map.getPlatform(x, y)
                        if platform in circle:
                            print("PLAT")
                            platform.kill()
                            platform.remove()

        """ ATUALIZANDO """
        # self.entities.update()

        """ DESENHANDO """
        self.screen.blit(self.background, (0, 0))
        # self.entities.draw(self.screen)

        self.menu.update(self.eventsTick)

        """ ATUALIZANDO TELA """
        pygame.display.flip()
        my.CLOCK.tick(my.FPS)


def runGame():
    game = Game()
    game.init()

    while game.running:
        game.loop()


from time import sleep

if __name__ == "__main__":
    try:
        runGame()
    except Exception as e:
        print(e)
        sleep(1000)
