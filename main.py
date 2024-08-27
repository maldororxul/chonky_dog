from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader
from widgets.menu_widget import MenuWidget
from widgets.game_session import GameSessionWidget
from widgets.sound_manager import SoundManager


class LoadingWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(LoadingWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text="Loading Chonky Dog...", font_size='20sp', halign='center'))


class MainGameWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainGameWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.sound_manager = SoundManager()
        self.menu_widget = MenuWidget(self.start_game, self.sound_manager)
        self.add_widget(self.menu_widget)
        self.sound_manager.play_menu_music()

    def start_game(self, level):
        self.sound_manager.stop_menu_music()
        self.sound_manager.play_game_music(level)
        self.clear_widgets()
        self.game_session_widget = GameSessionWidget(self.return_to_menu, self.debug_mode, self.sound_manager, level)
        self.add_widget(self.game_session_widget)
        self.game_session_widget.start_game()

    def debug_mode(self, instance):
        self.game_session_widget.debug_leave_last_pair()

    def return_to_menu(self, instance=None):
        self.sound_manager.stop_game_music()
        self.sound_manager.play_menu_music()
        self.clear_widgets()
        self.add_widget(self.menu_widget)


class ChonkyDog(App):
    def build(self):
        # Создаем виджет загрузки
        self.loading_widget = LoadingWidget()
        return self.loading_widget

    def on_start(self):
        # Начинаем предварительную загрузку ресурсов
        Clock.schedule_once(self.preload_resources, 0.1)

    def preload_resources(self, *args):
        # Список ресурсов для загрузки
        images = ['images/main.png', 'images/logo.png', 'images/level1/background.png']
        sounds = ['sounds/menu_music.mp3', 'sounds/game_music.mp3']

        # Предварительная загрузка изображений
        for img in images:
            CoreImage(img).texture

        # Предварительная загрузка звуков
        for snd in sounds:
            sound = SoundLoader.load(snd)
            if sound:
                sound.unload()  # Загружаем и выгружаем звук, чтобы проверить его доступность

        # Переход к отображению основного интерфейса после загрузки ресурсов
        Clock.schedule_once(self.show_main_screen, 0.1)

    def show_main_screen(self, *args):
        # Удаляем виджет загрузки и отображаем главное меню
        self.root.clear_widgets()
        self.root.add_widget(MainGameWidget())


if __name__ == '__main__':
    ChonkyDog().run()
