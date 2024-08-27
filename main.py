"""
    См. https://www.youtube.com/watch?v=s7kNe5o86yY
    см. Google AdMob, Unity Ads, Facebook Audience Network
    Google Play Billing API
    https://gist.github.com/zl475505/25245e8d28b13b3273e8bae1a63c4af2

    docker build -t kivy-android-builder-updated .
    docker run --rm -v "${PWD}:/home/user/hostcwd" kivy-android-builder-updated -v android debug
"""
from kivy.app import App
from kivy.core.window import Window
from widgets.menu_widget import MenuWidget
from widgets.game_session import GameSessionWidget
from kivy.uix.relativelayout import RelativeLayout
from widgets.sound_manager import SoundManager  # Импортируем SoundManager


class MainGameWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super(MainGameWidget, self).__init__(**kwargs)
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
        window_width = 360 * 1.2
        window_height = 640 * 1.2
        Window.size = (window_width, window_height)
        return MainGameWidget()


if __name__ == '__main__':
    ChonkyDog().run()
