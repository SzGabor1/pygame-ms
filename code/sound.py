import pygame
from settings import Settings


class Sounds():
    SOUNDS = {}
    VOLUME = 0.5  # You can set a default volume here if needed.

    @classmethod
    def load_sounds(cls, sound_names):
        for sound_name in sound_names:
            cls.SOUNDS[sound_name] = pygame.mixer.Sound(
                Settings.SOUNDS[sound_name])

    @classmethod
    def volume_validation(cls):
        if not 0 <= cls.VOLUME <= 1:
            cls.VOLUME = 0.5
        cls.update_volumes()

    @classmethod
    def update_volumes(cls):
        for sound in cls.SOUNDS.values():
            sound.set_volume(cls.VOLUME)

    @classmethod
    def set_static_volume(cls, amount):
        cls.VOLUME = amount
        cls.update_volumes()

    @classmethod
    def play(cls, sound_name):
        cls.SOUNDS[sound_name].play()

    @classmethod
    def play_loop(cls, sound_name):
        cls.SOUNDS[sound_name].play(-1)


# Initialize the Pygame mixer
pygame.mixer.init()
Sounds.set_static_volume(Settings.VOLUME)
# Load sounds and validate volume
Sounds.load_sounds(Settings.SOUNDS)
Sounds.volume_validation()
