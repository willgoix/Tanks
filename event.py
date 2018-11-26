import pygame, my, ui
from sys import exit


class EventManager:
    def __init__(self):
        self.events = []

    def get(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.showConfirmExitAlert()

    def showConfirmExitAlert(self):
        alertOpen = True
        alert = ui.ExitAlert()
        while alertOpen:
            alertOpen = alert.update()
            self.get()
            pygame.display.flip()

    def terminate(self):
        pygame.quit()
        exit()
