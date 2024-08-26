from kivy.uix.relativelayout import RelativeLayout
from widgets.control_widget import ControlWidget
from widgets.game_field import GameFieldWidget
from widgets.results_widget import ResultsWidget
from widgets.progress_manager import update_level_progress, load_progress, save_progress
from widgets.sound_manager import SoundManager


class GameSessionWidget(RelativeLayout):
    def __init__(self, end_game_callback, debug_callback, sound_manager, level, **kwargs):
        super(GameSessionWidget, self).__init__(**kwargs)
        self.sound_manager = sound_manager
        self.level = level

        self.control_widget = ControlWidget(end_game_callback, debug_callback, self.sound_manager)
        self.control_widget.pos_hint = {'top': 1}
        self.add_widget(self.control_widget)

        self.game_field = GameFieldWidget(sound_manager=self.sound_manager, level=self.level, size_hint=(1, 0.9))
        self.add_widget(self.game_field)

    def start_game(self):
        self.control_widget.start_timer()

    def end_game(self, instance=None):
        self.control_widget.stop_timer()

        # Получаем текущий уровень
        current_level = int(self.level[-1])

        # Обновляем прогресс игрока
        next_level = current_level + 1
        update_level_progress(current_level, self.control_widget.time)

        # Разблокируем следующий уровень, если он есть
        if next_level <= len(self.parent.menu_widget.level_buttons):
            progress = load_progress()
            progress['last_unlocked_level'] = next_level
            save_progress(progress)

        # Обновляем кнопки уровней в меню
        self.parent.menu_widget.update_level_buttons()

        # Возвращаемся в меню
        self.clear_widgets()
        self.show_results()

    def show_results(self):
        # Скрываем игровое поле и элементы управления перед отображением результата
        if self.game_field:
            self.game_field.opacity = 0  # Скрываем игровое поле
        if self.control_widget:
            self.control_widget.opacity = 0  # Скрываем элементы управления

        self.results_widget = ResultsWidget(self.close_results_callback)
        self.add_widget(self.results_widget)

    def close_results_callback(self, instance=None):
        print(0)

        # Удаляем ResultsWidget
        if self.results_widget:
            self.remove_widget(self.results_widget)
            print("ResultsWidget removed")

        # Принудительно удаляем все виджеты и добавляем снова
        self.clear_widgets()
        print("Cleared all widgets")

        # Добавляем обратно game_field и control_widget
        if self.game_field:
            self.game_field.opacity = 1  # Принудительно устанавливаем видимость
            self.add_widget(self.game_field)
            print("GameFieldWidget added")

        if self.control_widget:
            self.control_widget.opacity = 1  # Принудительно устанавливаем видимость
            self.add_widget(self.control_widget)
            print("ControlWidget added")

        # Проверка их видимости
        for child in self.children:
            print(f"Widget: {child}, Opacity: {child.opacity}")

        # Принудительно обновляем экран
        self.canvas.ask_update()

    def debug_leave_last_pair(self, instance=None):
        self.game_field.debug_leave_last_pair()
