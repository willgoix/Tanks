import pygame, my
from .ui import CENTER, IMAGES
from .widget import Widget
from functools import partial

CURSOR_NORMAL = pygame.cursors.arrow
CURSOR_HOVERED = pygame.cursors.broken_x
CURSOR_CLICKED = pygame.cursors.diamond


class Button(Widget):
    def __init__(self, onclick, pos, size, centralization=CENTER):
        Widget.__init__(self, pos, size, centralization)
        self.onclick = onclick
        self.surface = pygame.Surface(size)
        self.clicked = False
        self.hovered = False

    def asRect(self):
        return pygame.Rect(self.pos, self.size)

    def setText(self, text):
        self.text = text

    def click(self):
        if self.clicked: return False

        self.clicked = True
        self.onclick()

    def unclick(self):
        if not self.clicked: return False

        self.clicked = False

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            my.ENGINE.setCursor(IMAGES['cursor_pressed'])
        elif event.type == pygame.MOUSEBUTTONUP:
            my.ENGINE.setCursor(IMAGES['cursor'])


class TextButton(Button):
    def __init__(self, onclick, pos, size, text="", color=my.BLACK, centralization=CENTER):
        Button.__init__(self, onclick, pos, size, centralization)

        self.text = text
        self.color = color
        self.color_pressed = self._get_darker_color(80)
        self.color_hovered = self._get_darker_color(20)

    def _get_darker_color(self, percentage):
        """ Retorna uma cor X% mais escura """

        r, g, b, *_ = tuple(self.color)
        const = percentage / 100
        r = int(const * r)
        g = int(const * g)
        b = int(const * b)

        return (r, g, b)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos in self:
                self.click()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.unclick()

        elif event.type == pygame.MOUSEMOTION:
            if event.pos in self:
                self.hovered = True
            else:
                self.hovered = False

        Button.update(self, event)

    def render(self, screen):
        if self.clicked:
            color = self.color_pressed
        elif self.hovered:
            color = self.color_hovered
        else:
            color = self.color

        self.surface.fill(color)
        screen.blit(self.surface, self.pos)

        fontSurface = my.FONT(12).render(self.text, True, [0, 0, 0])
        centralizedX = self.pos[0] + self.surface.get_width() / 2 - fontSurface.get_width() / 2
        centralizedY = self.pos[1] + self.surface.get_height() / 2 - fontSurface.get_height() / 2

        screen.blit(fontSurface, (centralizedX, centralizedY))


class ImageButton(Button):
    def __init__(self, onclick, pos, text, image_surface, image_pressed=None, image_hovered=None,
                 centralization=CENTER):
        Button.__init__(self, onclick, pos, image_surface.get_size(), centralization)

        self.text = text
        self.image = pygame.transform.smoothscale(image_surface, self.size)

        if image_pressed is None:
            self.image_pressed = self._get_darker_image(80)
        else:
            self.image_pressed = pygame.transform.smoothscale(image_pressed, self.size)

        if image_hovered is None:
            self.image_hovered = self._get_darker_image(20)
        else:
            self.image_hovered = pygame.transform.smoothscale(image_hovered, self.size)

    def _get_darker_image(self, percentage):
        """ Retorna uma imagem X% mais escura """
        image_dark = self.image.copy()

        for x in range(self.size[0]):
            for y in range(self.size[1]):
                r, g, b, *_ = tuple(self.image.get_at((x, y)))
                const = (100 - percentage) / 100
                r = int(const * r)
                g = int(const * g)
                b = int(const * b)
                image_dark.set_at((x, y), (r, g, b))

        return image_dark

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos in self:
                self.click()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.unclick()

        elif event.type == pygame.MOUSEMOTION:
            if event.pos in self:
                self.hovered = True
            else:
                self.hovered = False

        Button.update(self, event)

    def render(self, screen):
        if self.clicked:
            image = self.image_pressed
        elif self.hovered:
            image = self.image_hovered
        else:
            image = self.image

        screen.blit(image, self.pos)

        fontSurface = my.FONT(int(image.get_height() - (79 % image.get_height()))).render(self.text, True, [0, 0, 0])
        centralizedX = self.pos[0] + image.get_width() / 2 - fontSurface.get_width() / 2
        centralizedY = self.pos[1] + image.get_height() / 2 - fontSurface.get_height() / 2

        screen.blit(fontSurface, (centralizedX, centralizedY))


class Drop(ImageButton):

    def __init__(self, ui, contentsName, onselect, pos, text, image_surface, image_pressed=None, image_hovered=None,
                 down=True, centralization=CENTER):
        ImageButton.__init__(self, onselect, pos, text, image_surface, image_pressed, image_hovered, centralization)
        self.ui = ui
        self.contents = contentsName
        self.contentsButtons = []

        self.image_arrow = IMAGES['arrow_down'] if down else IMAGES['arrow_up']

    def adaptSelectFunction(self, value):
        self.onclick(value)
        self.deleteContentButtons()

    def deleteContentButtons(self):
        self.image_arrow = IMAGES['arrow_down']

        for contentButton in self.contentsButtons:
            self.ui.removeWidget(contentButton)
        self.contentsButtons.clear()

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos in self:
                self.clicked = True

                if len(self.contentsButtons) == 0:
                    self.image_arrow = IMAGES['arrow_up']

                    for content in range(0, len(self.contents)):
                        image = IMAGES['dropdown_mid']

                        if content == 0:
                            image = IMAGES['dropdown_mid']  # dropdown_top
                        elif content == len(self.contents) - 1:
                            image = IMAGES['dropdown_bottom']

                        button = ImageButton(partial(self.adaptSelectFunction, self.contents[content]),
                                             (self.pos[0] + self.size[0] / 2,
                                              self.pos[1] + self.size[1] + 12 + content * 24), self.contents[content],
                                             image)
                        self.contentsButtons.append(button)
                        self.ui.addWidget(button)
                else:
                    self.deleteContentButtons()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.unclick()

        elif event.type == pygame.MOUSEMOTION:
            if event.pos in self:
                self.hovered = True
            else:
                self.hovered = False

        Button.update(self, event)

    def render(self, screen):
        ImageButton.render(self, screen)
        screen.blit(self.image_arrow, (self.pos[0] + self.size[0] - 25, self.pos[1] + self.size[1] / 2 - 5))
