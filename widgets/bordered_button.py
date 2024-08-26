from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class BorderedButton(Button):
    def __init__(self, **kwargs):
        super(BorderedButton, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0, 0, 1)  # Черная граница
            self.rect_black = Rectangle(size=self.size, pos=self.pos)
            Color(1, 1, 1, 1)  # Белая граница
            self.rect_white = Rectangle(size=(self.size[0] - 4, self.size[1] - 4),
                                        pos=(self.pos[0] + 2, self.pos[1] + 2))
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect_black.pos = self.pos
        self.rect_black.size = self.size
        self.rect_white.pos = (self.pos[0] + 2, self.pos[1] + 2)
        self.rect_white.size = (self.size[0] - 4, self.size[1] - 4)
