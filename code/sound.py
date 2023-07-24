import pygame


class Sounds():
    def __init__(self, settings, sound_names):
        self.sounds = {}
        self.settings = settings
        self.load_sounds(sound_names)
        self.set_volume(self.settings.VOLUME)

    def __getitem__(self, sound_name):
        return self.sounds[sound_name]

    def load_sounds(self, sound_names):
        for tag in sound_names:
            self.sounds[tag] = pygame.mixer.Sound(self.settings.SOUNDS[tag])

        # self.sounds['sword'] = pygame.mixer.Sound('audio/sword.wav')
        # self.sounds['main'] = pygame.mixer.Sound('audio/main.mp3')

    def set_volume(self, amount):
        for sound in self.sounds.values():
            sound.set_volume(amount)

    def play(self, tag):
        self.sounds[tag].play()

    def play_loop(self, tag):
        self.sounds[tag].play(-1)
