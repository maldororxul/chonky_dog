from kivy.core.audio import SoundLoader

class SoundManager:
    def __init__(self):
        self.flip_sound = SoundLoader.load('sounds/flip.wav')
        self.match_sound = SoundLoader.load('sounds/match.wav')
        self.button_sound = SoundLoader.load('sounds/button.wav')
        self.win_sound = SoundLoader.load('sounds/win.wav')

        self.menu_music = SoundLoader.load('music/menu_music.mp3')
        self.win_music = SoundLoader.load('music/win_music.mp3')
        self.game_music = None

        # Настройка громкости
        if self.menu_music:
            self.menu_music.volume = 0.7
        if self.flip_sound:
            self.flip_sound.volume = 1.0
        if self.match_sound:
            self.match_sound.volume = 1.0
        if self.button_sound:
            self.button_sound.volume = 1.0
        if self.win_sound:
            self.win_sound.volume = 1.0

    def play_button_sound(self):
        if self.button_sound:
            self.button_sound.play()

    def play_flip_sound(self):
        if self.flip_sound:
            self.flip_sound.play()

    def play_match_sound(self):
        if self.match_sound:
            self.match_sound.play()

    def play_win_sound(self):
        if self.win_sound:
            self.win_sound.play()

    def play_menu_music(self):
        if self.game_music:
            self.game_music.stop()
        if self.menu_music:
            self.menu_music.loop = True
            self.menu_music.play()

    def play_game_music(self, level):
        if self.menu_music:
            self.menu_music.stop()
        self.game_music = SoundLoader.load(f'music/{level}.mp3')
        if self.game_music:
            self.game_music.volume = 0.7
            self.game_music.loop = True
            self.game_music.play()

    def stop_menu_music(self):
        if self.menu_music:
            self.menu_music.stop()

    def stop_game_music(self):
        if self.game_music:
            self.game_music.stop()
        if self.win_music:
            self.win_music.stop()
