from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.image import Image

from widgets.bordered_button import BorderedButton
from widgets.progress_manager import load_progress, get_level_info  # Импортируем функцию для загрузки прогресса
from widgets.sound_manager import SoundManager


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

    def create_header(self):
        # Логотип
        logo = Image(source='images/logo.png', size_hint=(None, None), size=(300, 300),
                     pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(logo)

        # Текст "SELECT LEVEL"
        # label = Label(text="SELECT LEVEL", font_size=24, color=(1, 1, 1, 1),
        #               size_hint=(None, None), size=(200, 50),
        #               pos_hint={'center_x': 0.5, 'y': 0.8})
        # self.add_widget(label)

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
            button = BorderedButton(size_hint=(0.25, 0.25), pos_hint={'center_x': 0.3 + i * 0.4, 'center_y': 0.5},
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
