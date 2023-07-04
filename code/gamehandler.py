import pygame

from level import Level
from save import Save
from ingame_menu import IngameMenu


class GameHandler():
    def __init__(self, settings, what_to_load):
        self.save = Save(what_to_load)
        self.game_paused = False
        self.settings = settings
        self.level = Level(self.settings, self.save.load_data())
        self.ingame_menu = IngameMenu(
            self.settings, self.pause_game, self.save_game)

    def run(self):
        if self.game_paused:
            self.ingame_menu.display()
        else:
            self.level.run()

    def save_game(self):
        print("gamehandler save")
        self.save.create_save(self.level.player)

    def pause_game(self):
        self.game_paused = not self.game_paused
