import math
import os
import re
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
import random

from widgets.bordered_button import BorderedButton

# Константы для соотношения сторон игрового поля
ASPECT_RATIO_WIDTH = 9
ASPECT_RATIO_HEIGHT = 15

class GameFieldWidget(RelativeLayout):
    def __init__(self, sound_manager, level, **kwargs):
        super(GameFieldWidget, self).__init__(**kwargs)
        self.sound_manager = sound_manager
        self.level = level

        # Определяем ширину экрана
        screen_width = Window.width

        # Рассчитываем высоту игрового поля с учетом соотношения сторон
        field_height = screen_width * (ASPECT_RATIO_HEIGHT / ASPECT_RATIO_WIDTH)

        # Устанавливаем размеры игрового поля
        self.size_hint = (None, None)
        self.size = (screen_width, field_height)

        # Определяем путь к папке с изображениями уровня
        self.images_path = f'images/{self.level}'

        # Регулярное выражение для поиска файлов вида cardX.png
        card_pattern = re.compile(r'card\d+\.png')

        # Считываем количество изображений, подходящих под шаблон
        card_images = [name for name in os.listdir(self.images_path) if card_pattern.match(name)]
        self.num_images = len(card_images)

        # Убедимся, что количество изображений четное
        if self.num_images % 2 != 0:
            raise ValueError("Количество изображений должно быть четным!")

        # Создаем основной контейнер для всех виджетов
        layout = RelativeLayout(size_hint=(None, None), size=(screen_width, field_height))
        self.add_widget(layout)

        # Загрузка фонового изображения и его добавление на задний план
        self.bg_image = Image(source=f'{self.images_path}/background.png', allow_stretch=True, keep_ratio=True,
                              size_hint=(None, None), size=(screen_width, field_height))
        layout.add_widget(self.bg_image)

        # Вычисляем количество строк и столбцов для сетки
        grid_size = math.ceil(math.sqrt(self.num_images * 2))  # так как каждая карточка будет дважды
        rows = grid_size
        cols = grid_size

        # Создание сетки для карточек и её добавление поверх фона
        self.grid = GridLayout(cols=cols, rows=rows, spacing=0, padding=0, size_hint=(None, None),
                               size=(screen_width, field_height))
        layout.add_widget(self.grid)

        # Построение игрового поля
        self.build_field()

    def build_field(self):
        images = list(range(1, self.num_images + 1)) * 2
        random.shuffle(images)
        self.cards = []

        for img in images:
            btn = BorderedButton(on_press=self.reveal_card, background_normal=f'{self.images_path}/card_back.png',
                         background_down=f'{self.images_path}/card_back.png')
            btn.img = f'{self.images_path}/card{img}.png'
            btn.revealed = False
            btn.opacity = 1
            btn.size_hint = (1 / self.grid.cols, 1 / self.grid.rows)
            self.grid.add_widget(btn)
            self.cards.append(btn)

        self.opened_cards = []
        self.matched_pairs = 0

    def reveal_card(self, btn):
        if btn.revealed or len(self.opened_cards) == 2:
            return

        self.sound_manager.play_flip_sound()

        btn.background_normal = btn.img
        btn.revealed = True
        self.opened_cards.append(btn)

        if len(self.opened_cards) == 2:
            if self.opened_cards[0].img == self.opened_cards[1].img:
                Clock.schedule_once(self.hide_matched_cards, 0.5)
                self.matched_pairs += 1

                self.sound_manager.play_match_sound()

                if self.matched_pairs == len(self.cards) // 2:
                    self.sound_manager.play_win_sound()
                    self.sound_manager.stop_game_music()
                    Clock.schedule_once(lambda dt: self.parent.end_game(), 0.5)
            else:
                Clock.schedule_once(self.hide_cards, 0.5)

    def hide_cards(self, dt):
        for btn in self.opened_cards:
            btn.background_normal = f'images/{self.level}/card_back.png'
            btn.revealed = False
        self.opened_cards.clear()

    def hide_matched_cards(self, dt):
        for btn in self.opened_cards:
            btn.opacity = 0
            btn.disabled = True
        self.opened_cards.clear()

    def debug_leave_last_pair(self):
        if len(self.cards) < 2:
            return

        # Находим две карточки с одинаковыми изображениями
        last_pair = None
        for i in range(len(self.cards)):
            for j in range(i + 1, len(self.cards)):
                if self.cards[i].img == self.cards[j].img:
                    last_pair = (self.cards[i], self.cards[j])
                    break
            if last_pair:
                break

        if last_pair:
            for btn in self.cards:
                if btn not in last_pair:
                    btn.opacity = 0
                    btn.disabled = True
                    btn.revealed = True  # Делаем карточку "угаданной"
                    self.matched_pairs += 1  # Увеличиваем счетчик угаданных пар
            # Обновляем количество угаданных пар
            self.matched_pairs = len(self.cards) // 2 - 1
            # Теперь симулируем, что последняя пара угадана игроком
            self.reveal_card(last_pair[0])
