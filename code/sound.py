import pygame
from settings import Settings


class Sounds():
    VOLUME = 0.5

    SOUNDS = {}

    @classmethod
    def load_sounds(cls, sound_names):
        for sound_name in sound_names:
            cls.SOUNDS[sound_name] = pygame.mixer.Sound(
                Settings.SOUNDS[sound_name])

    def __init__(self):
        self.volume_validation()
        self.update_volumes()

    def volume_validation(self):
        if not 0 <= Settings.VOLUME <= 1:
            Settings.VOLUME = 0.5

    def update_volumes(self):
        for sound in Sounds.SOUNDS.values():
            sound.set_volume(Settings.VOLUME)

    @classmethod
    def set_static_volume(cls, amount):
        cls.VOLUME = amount
        # Call the instance method directly without using cls
        Sounds().update_volumes()

    @classmethod
    def play(cls, sound_name):
        cls.SOUNDS[sound_name].play()

    @classmethod
    def play_loop(cls, sound_name):
        cls.SOUNDS[sound_name].play(-1)


# Load the sounds using the sound names from the Settings class
Sounds.load_sounds(Settings.SOUNDS)
