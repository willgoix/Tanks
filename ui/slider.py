from .widget import Widget
from .ui import CENTER


class SlibeBar(Widget):

    def __init__(self, onchange, pos, size, min_=0, max_=100, step=1, image_left=ui, image_center=ui, image_right=ui, centralization=CENTER):
        Widget.__init__(self, pos, size, centralization)
        self.onchange = onchange
        self.min_ = min_
        self.max_ = max_
        self.step = step

    def update(self, event):
        pass

    def render(self, screen):
        screen.blit(self.font.render(self.text, True, (0, 0, 0)), self.pos)
