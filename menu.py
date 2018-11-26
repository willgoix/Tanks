import pygame, math
from ui import ui, button
import my


class Menu(ui.UI):
    def __init__(self, screen):
        ui.UI.__init__(self, screen)

        self.addWidget(button.TextButton(lambda: self.oncl(), [50, 50], (100, 50), text="Teste", color=(40, 244, 10)))
        self.button = button.ImageButton(lambda: self.oncl(), [10, my.SCREEN_HEIGHT], text="Botão",
                                         image_surface=pygame.image.load("assets/ui/button.png"),
                                         image_pressed=pygame.image.load("assets/ui/button_pressed.png"))
        self.addWidget(self.button)
        self.animation = True

    def update(self, events):
        self.screen.fill(my.TURQUOISE)
        super().update(events)

        if self.animation:
            if self.button.pos[1] > my.SCREEN_HEIGHT / 2:
                self.button.pos[1] -= math.fabs(my.SCREEN_HEIGHT / 2 + 300 - self.button.pos[1]) * 0.1
        else:
            if self.button.pos[1] < my.SCREEN_HEIGHT - 1:
                self.button.pos[1] += (my.SCREEN_HEIGHT + 50 - self.button.pos[1]) * 0.1

    def oncl(self):
        self.animation = False
        print("click")
