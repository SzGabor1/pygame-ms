import pygame

from level import Level
from save import Save


class GameHandler():
    def __init__(self, settings):
        self.settings = settings
        self.level = Level(self.settings)
        #self.save = Save()

    def run(self):
        self.level.run()
