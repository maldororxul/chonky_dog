from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from widgets.sound_manager import SoundManager


class ControlWidget(RelativeLayout):
    timer_label = ObjectProperty(None)
    exit_button = ObjectProperty(None)
    debug_button = ObjectProperty(None)

    def __init__(self, end_game_callback, debug_callback, sound_manager, **kwargs):
        super(ControlWidget, self).__init__(**kwargs)
        self.sound_manager = sound_manager  # Сохраняем ссылку на SoundManager
        self.size_hint = (1, None)
        self.height = 50

        # Белый цвет текста и черный фон
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0, 0, 1)  # Черный фон
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(pos=self.update_rect, size=self.update_rect)

        self.timer_label = Label(text="00:00", color=(1, 1, 1, 1), font_size=24, size_hint=(0.20, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.timer_label.size = self.timer_label.texture_size
        self.add_widget(self.timer_label)

        self.exit_button = Button(
            text="CLOSE",
            size=(Window.width * 0.2, Window.height * 0.05),  # Фиксированные размеры в зависимости от экрана
            size_hint=(None, None),  # Отключение size_hint
            pos_hint={'right': 0.95, 'top': 0.9}
        )
        self.exit_button.bind(on_press=end_game_callback)
        self.exit_button.bind(on_press=lambda instance: self.sound_manager.play_button_sound())  # Звук кнопки
        self.add_widget(self.exit_button)

        # Кнопка для отладки
        # self.debug_button = Button(text="!!", size_hint=(0.1, 0.1), size=(50, 50), pos_hint={'x': 0, 'top': 1})
        # self.debug_button.bind(on_press=debug_callback)
        # self.debug_button.bind(on_press=lambda instance: self.sound_manager.play_button_sound())  # Звук кнопки
        # self.add_widget(self.debug_button)

        self.time = 0
        self.clock_event = None

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def start_timer(self):
        self.time = 0
        self.clock_event = Clock.schedule_interval(self.update_timer, 1)

    def stop_timer(self):
        if self.clock_event:
            Clock.unschedule(self.clock_event)

    def update_timer(self, dt):
        self.time += 1
        minutes = self.time // 60
        seconds = self.time % 60
        self.timer_label.text = f"{minutes:02}:{seconds:02}"
        self.timer_label.size = self.timer_label.texture_size
