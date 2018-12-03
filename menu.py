import pygame, math, my, sound, game, threading, loading, random, lib.delayedfunc
from ui import ui, button, label, slider, checker, bar, input
from functools import partial

BACKGROUND = None


class Menu(ui.UI):

    def __init__(self, screen):
        ui.UI.__init__(self, screen)
        global BACKGROUND
        BACKGROUND = pygame.transform.scale(ui.IMAGES['background'], my.SCREEN_SIZE)

        self.logo = label.Image([my.SCREEN_HALF_WIDTH, -my.SCREEN_HEIGHT], pygame.image.load("assets/logo.png"),
                                centralization=ui.BOTTOM)
        self.addWidget(self.logo)

        self.playOfflineButton = button.ImageButton(lambda: self.playOffline(),
                                                    [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
                                                    text="Jogar Offline",
                                                    image_surface=ui.IMAGES['button'],
                                                    image_pressed=ui.IMAGES['button_pressed'])
        self.playOnlineButton = button.ImageButton(lambda: self.playOnline(),
                                                   [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
                                                   text="Jogar Online",
                                                   image_surface=ui.IMAGES['button'],
                                                   image_pressed=ui.IMAGES['button_pressed'])
        self.optionsButton = button.ImageButton(lambda: self.options(),
                                                [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
                                                text="Opções",
                                                image_surface=ui.IMAGES['button'],
                                                image_pressed=ui.IMAGES['button_pressed'])
        self.creditsButton = button.ImageButton(lambda: self.credits(),
                                                [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT],
                                                text="Créditos",
                                                image_surface=ui.IMAGES['button'],
                                                image_pressed=ui.IMAGES['button_pressed'])
        self.addWidget(self.playOfflineButton)
        self.addWidget(self.playOnlineButton)
        self.addWidget(self.optionsButton)
        self.addWidget(self.creditsButton)
        self.addWidget(label.Text([my.SCREEN_WIDTH - 5, my.SCREEN_HEIGHT], "Tanks v" + my.VERSION, 20,
                                  centralization=ui.LEFT | ui.UPPER))

        self.animation = True
        self.readyToNext = False
        self.next = self

    def update(self, events):
        self.screen.blit(BACKGROUND, (0, 0))
        ui.UI.update(self, events)

        if self.animation:
            # TO UP
            y = 0
            for button in (self.playOfflineButton, self.playOnlineButton, self.optionsButton, self.creditsButton):
                if button.pos[1] > my.SCREEN_HALF_HEIGHT + y:
                    button.pos[1] -= int(math.fabs(my.SCREEN_HALF_HEIGHT + y - button.pos[1]) * 0.1)
                    y += 60

            # TO DOWN
            if self.logo.pos[1] < 0:
                self.logo.pos[1] += math.fabs(self.logo.pos[1]) * 0.1
        else:
            # TO UP
            y = 0
            for button in (self.playOfflineButton, self.playOnlineButton, self.optionsButton, self.creditsButton):
                if button.pos[1] < my.SCREEN_HEIGHT:
                    button.pos[1] += (my.SCREEN_HEIGHT + y - button.pos[1]) * 0.1
                    y += 60

            # TO DOWN
            if self.logo.pos[1] < 0:
                self.logo.pos[1] += math.fabs(self.logo.pos[1]) * 0.1

        return self.next

    def playOffline(self):
        sound.play('click')
        self.animation = False
        self.next = PlayOfflineMenu(self.screen)

    def playOnline(self):
        sound.play('click')
        self.animation = False
        self.next = PlayOnlineMenu(self.screen)

    def options(self):
        sound.play('click')
        self.animation = False
        self.next = OptionsMenu(self.screen)

    def credits(self):
        sound.play('click')
        self.animation = False
        self.next = CreditsMenu(self.screen)


class PlayOfflineMenu(ui.UI):
    def __init__(self, screen):
        ui.UI.__init__(self, screen)

        self.addWidget(label.Text([50, 50], "Configure o jogo:", fontsize=18, centralization=ui.RIGHT))

        self.addWidget(input.TextBox(partial(self.inputName), [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT // 6], [200, 30],
                                     'Digite seu nicknme',
                                     box_image=ui.IMAGES['button']))
        self.nickname = 'Jogador'

        self.enemiesValue = label.Text([my.SCREEN_HALF_WIDTH + 50, my.SCREEN_HALF_HEIGHT // 2 + 40], "5", fontsize=18)
        self.addWidget(self.enemiesValue)
        self.addWidget(label.Text([my.SCREEN_HALF_WIDTH - 10, my.SCREEN_HALF_HEIGHT // 2 + 40], "Inimigos", fontsize=18))
        self.addWidget(slider.SliderBar(partial(self.sliderEnemies), [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT // 3 + 32], (200, 5),
                                        min=1, max=10, step=1,
                                        initial=5,
                                        image_slider=ui.IMAGES['slider'],
                                        image_pointer=ui.IMAGES['slider_pointer']))

        self.addWidget(button.ImageButton(lambda: self.back(),
                                          [my.SCREEN_HALF_WIDTH - 20, my.SCREEN_HEIGHT - (my.SCREEN_HEIGHT // 6)],
                                          text="Voltar",
                                          image_surface=ui.IMAGES['button'],
                                          image_pressed=ui.IMAGES['button_pressed'],
                                          centralization=ui.LEFT))
        self.addWidget(button.ImageButton(lambda: self.startGame(),
                                          [my.SCREEN_HALF_WIDTH + 20, my.SCREEN_HEIGHT - (my.SCREEN_HEIGHT // 6)],
                                          text="Iniciar Jogo",
                                          image_surface=ui.IMAGES['button_green'],
                                          image_pressed=ui.IMAGES['button_green_pressed'],
                                          centralization=ui.RIGHT))

        self.next = self

    def update(self, events):
        self.screen.blit(BACKGROUND, (0, 0))
        ui.UI.update(self, events)

        return self.next

    def sliderEnemies(self, value):
        self.enemiesValue.text = str(value)

    def inputName(self, value):
        self.nickname = str(value)

    def back(self):
        self.next = Menu(self.screen)

    def startGame(self):
        # TODO: Configurável o tamanho
        def start():
            gameConfigurations = [int(self.enemiesValue.text)]
            playerConfigurations = [self.nickname]
            mapConfigurations = [400, 400, random.randint(1000, 10000)]

            my.ENGINE.game = game.GameOffline(gameConfigurations, playerConfigurations, mapConfigurations)
            my.ENGINE.game.start()

        threadStarting = threading.Thread(target=start)
        threadStarting.start()

        my.ENGINE.game.hud = loading.Loading(my.ENGINE.screen)  # Ás vezes não carrega a tempo...
        self.next = my.ENGINE.game.hud


class PlayOnlineMenu(ui.UI):
    def __init__(self, screen):
        ui.UI.__init__(self, screen)

        self.addWidget(label.Text(my.SCREEN_HALF_SIZE, "Em desenvolvimento...", fontsize=24))
        self.addWidget(button.ImageButton(lambda: self.back(),
                                          [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT - (my.SCREEN_HEIGHT // 6)],
                                          text="Voltar",
                                          image_surface=ui.IMAGES['button'],
                                          image_pressed=ui.IMAGES['button_pressed']))

        # self.input = input.TextBox(partial(self.input), [my.SCREEN_HALF_WIDTH, 100], [200,30], 'Digite aqui', box_image=ui.IMAGES['button'])
        # self.addWidget(self.input)

        self.next = self

    def update(self, events):
        self.screen.blit(BACKGROUND, (0, 0))
        ui.UI.update(self, events)

        return self.next

    def back(self):
        self.next = Menu(self.screen)


class OptionsMenu(ui.UI):
    def __init__(self, screen):
        ui.UI.__init__(self, screen)

        self.fpsValue = label.Text([my.SCREEN_HALF_WIDTH + 25, my.SCREEN_HEIGHT // 6], str(my.FPS), fontsize=20)
        self.addWidget(self.fpsValue)
        self.addWidget(label.Text([my.SCREEN_HALF_WIDTH - 25, my.SCREEN_HEIGHT // 6], "FPS", fontsize=20))
        self.addWidget(
            slider.SliderBar(partial(self.sliderFps), [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT // 4], (300, 5), min=20,
                             max=100, step=1,
                             initial=my.FPS,
                             image_slider=ui.IMAGES['slider'],
                             image_pointer=ui.IMAGES['slider_pointer']))

        contents = []
        modes = pygame.display.list_modes()
        for mode in range(0, len(modes) - 5):  # -5 = Tirando os 5 menores valores pois é pequeno até demais pro jogo
            contents.append(str(modes[mode][0]) + ' x ' + str(modes[mode][1]) + (' (FULL)' if mode == 0 else ''))
        self.addWidget(button.Drop(self, contents,
                                   partial(self.selectResolution),
                                   [my.SCREEN_HALF_WIDTH, my.SCREEN_HALF_HEIGHT - 50],
                                   text="Resolução",
                                   image_surface=ui.IMAGES['button'],
                                   image_pressed=ui.IMAGES['button_pressed'],
                                   down=True))

        self.addWidget(
            label.Text([my.SCREEN_HALF_WIDTH + 30, my.SCREEN_HALF_HEIGHT], "Acelerar CPU (tela cheia)", fontsize=20))
        self.addWidget(checker.Checker(partial(self.checkedHardware),
                                       [my.SCREEN_HALF_WIDTH - 150, my.SCREEN_HALF_HEIGHT],
                                       checked=my.HARDWARE_ACCELERATED,
                                       image=ui.IMAGES['box'],
                                       image_checked=ui.IMAGES['box_checked']))

        self.addWidget(
            label.Text([my.SCREEN_HALF_WIDTH + 20, my.SCREEN_HALF_HEIGHT + 40], "Áudio, sons e vozes", fontsize=20))
        self.addWidget(checker.Checker(partial(self.checkedAudio),
                                       [my.SCREEN_HALF_WIDTH - 150, my.SCREEN_HALF_HEIGHT + 40],
                                       checked=not my.MUTED,
                                       image=ui.IMAGES['box'],
                                       image_checked=ui.IMAGES['box_checked']))

        self.addWidget(button.ImageButton(lambda: self.back(),
                                          [my.SCREEN_HALF_WIDTH - 20, my.SCREEN_HEIGHT - (my.SCREEN_HEIGHT // 6)],
                                          text="Voltar",
                                          image_surface=ui.IMAGES['button'],
                                          image_pressed=ui.IMAGES['button_pressed'],
                                          centralization=ui.LEFT))
        self.addWidget(button.ImageButton(lambda: self.save(),
                                          [my.SCREEN_HALF_WIDTH + 20, my.SCREEN_HEIGHT - (my.SCREEN_HEIGHT // 6)],
                                          text="Salvar",
                                          image_surface=ui.IMAGES['button_green'],
                                          image_pressed=ui.IMAGES['button_green_pressed'],
                                          centralization=ui.RIGHT))
        self.next = self

    def update(self, events):
        self.screen.blit(BACKGROUND, (0, 0))
        ui.UI.update(self, events)

        return self.next

    def sliderFps(self, value):
        self.fpsValue.text = str(value)
        my.CONFIG.set('fps', value)

    def selectResolution(self, value):
        if '(FULL)' in value:
            my.CONFIG.set('windowed', False)
            my.CONFIG.set('screen_width', int(value.split(" x ")[0]))
            my.CONFIG.set('screen_height', int(value.split(" x ")[1].split(" ")[0]))
        else:
            my.CONFIG.set('windowed', True)
            my.CONFIG.set('screen_width', int(value.split(" x ")[0]))
            my.CONFIG.set('screen_height', int(value.split(" x ")[1]))

    def checkedHardware(self, value):
        my.CONFIG.set('hardware_accelerated', value)

    def checkedAudio(self, value):
        my.CONFIG.set('muted', not value)

    def back(self):
        self.next = Menu(self.screen)

    def save(self):
        my.FPS = my.CONFIG.get('fps')
        my.HARDWARE_ACCELERATED = my.CONFIG.get('hardware_accelerated')
        my.MUTED = my.CONFIG.get('muted')

        oldwidth, oldwindowed = my.SCREEN_WIDTH, my.WINDOWED
        my.WINDOWED = my.CONFIG.get('windowed')
        my.SCREEN_WIDTH = my.CONFIG.get('screen_width')
        my.SCREEN_HEIGHT = my.CONFIG.get('screen_height')
        my.SCREEN_HALF_WIDTH = my.CONFIG.get('screen_width') / 2
        my.SCREEN_HALF_HEIGHT = my.CONFIG.get('screen_height') / 2
        my.SCREEN_SIZE = (my.SCREEN_WIDTH, my.SCREEN_HEIGHT)
        my.SCREEN_HALF_SIZE = (my.SCREEN_HALF_WIDTH, my.SCREEN_HALF_HEIGHT)
        if my.CONFIG.get('screen_width') != oldwidth or my.CONFIG.get('windowed') != oldwindowed:
            my.ENGINE.adaptScreen()

        my.CONFIG.save()
        self.next = Menu(self.screen)


class CreditsMenu(ui.UI):
    def __init__(self, screen):
        ui.UI.__init__(self, screen)

        self.addWidget(label.Text([my.SCREEN_HALF_WIDTH, 100], "Desenvolvido por:", fontsize=24))
        self.addWidget(label.Text([my.SCREEN_HALF_WIDTH, 140], "Willian Gois ~the coder guy", fontsize=20))
        self.addWidget(label.Text([my.SCREEN_HALF_WIDTH, 160], "Lucas Verona ~the h4ck3r m4n", fontsize=20))

        self.addWidget(label.Text([my.SCREEN_HALF_WIDTH, 220], "Texturas por:", fontsize=24))
        self.addWidget(label.Text([my.SCREEN_HALF_WIDTH, 260], "(UI): Kenney Vleugels (www.kenney.nl)", fontsize=20))

        self.addWidget(button.ImageButton(lambda: self.back(),
                                          [my.SCREEN_HALF_WIDTH, my.SCREEN_HEIGHT - (my.SCREEN_HEIGHT // 6)],
                                          text="Voltar",
                                          image_surface=ui.IMAGES['button'],
                                          image_pressed=ui.IMAGES['button_pressed']))

        self.next = self

    def update(self, events):
        self.screen.blit(BACKGROUND, (0, 0))
        ui.UI.update(self, events)

        return self.next

    def back(self):
        self.next = Menu(self.screen)
