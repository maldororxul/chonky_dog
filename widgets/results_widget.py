from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class ResultsWidget(RelativeLayout):
    def __init__(self, close_callback, **kwargs):
        super(ResultsWidget, self).__init__(**kwargs)
        self.size_hint = (0.5, 0.5)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.close_callback = close_callback

        self.add_widget(Label(text="Victory!", size_hint=(1, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        close_button = Button(
            text="CLOSE",
            size=(Window.width * 0.2, Window.height * 0.05),  # Фиксированные размеры в зависимости от экрана
            size_hint=(None, None),  # Отключение size_hint
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        # close_button = Button(text="Close", size_hint=(0.5, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        close_button.bind(on_press=self.close_results)
        self.add_widget(close_button)

    def close_results(self, instance):
        # Удаляем ResultsWidget из родительского виджета
        self.parent.remove_widget(self)
        # Вызываем коллбэк для восстановления видимости других виджетов
        if self.close_callback:
            self.close_callback()
