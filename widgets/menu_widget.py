from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from widgets.bordered_button import BorderedButton
from widgets.progress_manager import get_level_info

class MenuWidget(RelativeLayout):
    def __init__(self, start_game_callback, sound_manager, **kwargs):
        super(MenuWidget, self).__init__(**kwargs)
        self.sound_manager = sound_manager
        self.start_game_callback = start_game_callback

        # Установка фона
        self.bg_image = Image(source='images/main.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg_image)

        self.level_buttons = []
        self.create_header()
        self.create_level_buttons()

        # Привязка метода on_size к событию изменения размера окна
        Window.bind(on_resize=self.on_size)

    def on_size(self, *args):
        # Обновление размеров и положения виджетов
        self.bg_image.size = self.size
        self.bg_image.pos = self.pos

        for i, button in enumerate(self.level_buttons):
            button.size_hint = (0.25, 0.25)  # Размер кнопок
            button.pos_hint = {'center_x': (i + 1) / (len(self.level_buttons) + 1), 'center_y': 0.5}  # Центровка по горизонтали с равными интервалами
        self.do_layout()

    def create_header(self):
        # Логотип
        logo = Image(source='images/logo.png', size_hint=(None, None), size=(Window.width * 0.35, Window.height * 0.35),
                     pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(logo)

    def create_level_buttons(self):
        levels = ['level1', 'level2']  # Добавьте больше уровней при необходимости

        # Удаляем старые кнопки
        for button in self.level_buttons:
            self.remove_widget(button)
        self.level_buttons.clear()

        # Цикл по всем уровням
        for i, level in enumerate(levels):
            level_info = get_level_info(level)
            bg_image_path = f'images/{level}/background.png'
            button = BorderedButton(size_hint=(0.25, 0.25), pos_hint={'center_x': (i + 1) / (len(levels) + 1), 'center_y': 0.5},
                            background_normal=bg_image_path)
            if not level_info['unlocked']:
                button.disabled = True  # Заблокировать уровень, если он еще не разблокирован
            else:
                button.bind(on_press=lambda instance, lvl=level: self.select_level(lvl))
            self.add_widget(button)
            self.level_buttons.append(button)

    def update_level_buttons(self):
        # Удаляем старые кнопки
        for button in self.level_buttons:
            self.remove_widget(button)
        self.level_buttons.clear()

        # Заново создаем кнопки уровней
        self.create_level_buttons()

    def select_level(self, level):
        self.sound_manager.play_button_sound()
        self.start_game_callback(level)
