import pygame, my, event, menu


class Engine:

    def __init__(self):
        """ PRE-RUN """
        pygame.init()
        if my.WINDOWED:
            self.screen = pygame.display.set_mode((my.SCREEN_WIDTH, my.SCREEN_HEIGHT))
        else:
            screenInfo = pygame.display.Info()
            my.SCREEN_WIDTH = screenInfo.current_w
            my.SCREEN_HEIGHT = screenInfo.current_h
            self.screen = pygame.display.set_mode((my.SCREEN_WIDTH, my.SCREEN_HEIGHT), pygame.FULLSCREEN)
        # pygame.display.set_icon(pygame.image.load('assets/tanks/tank_desert.png'))
        pygame.display.set_caption("Tanks - Iniciando...")

        """ LOADING SCREEN """
        self.screen.fill(my.MIDNIGHT_BLUE)
        pygame.display.update()

        self.clock = None
        self.event_manager = None
        self.interface = None
        self.running = True

    def run(self):
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.pre_init(44100, -16, 2, 1024)

        self.clock = pygame.time.Clock()
        self.event_manager = event.EventManager()
        self.interface = menu.Menu(self.screen)

        while self.running:
            self.event_manager.get()
            self.interface.update(self.event_manager.events)

            pygame.display.flip()

            self.clock.tick(my.FPS)
            pygame.display.set_caption("Tanks - FPS: ", str(self.clock.get_fps()))

engine = None

if __name__ == '__main__':
    engine = Engine()
    engine.run()
