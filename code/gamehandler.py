import pygame

from level import Level
from save import Save
from ingame_menu import IngameMenu, Ingame_settings
from menuenums import menuenums


class GameHandler():
    def __init__(self, settings, what_to_load):
        self.save = Save(what_to_load)
        self.game_paused = False
        self.settings = settings
        self.level = Level(self.settings, self.save.load_data())
        self.ingame_menu = IngameMenu(
            self.settings, self.pause_game, self.save_game, self.open_ingame_settings)

        self.is_settings_menu_open = False
        self.Ingame_settings = Ingame_settings(
            self.settings, self.open_ingame_settings)

        self.is_talent_menu_open = False
        self.talent_menu_open_time = None
        self.key_press_cooldown = 300

    def run(self):
        self.cooldown()
        if self.game_paused:
            if self.is_settings_menu_open:
                self.Ingame_settings.render()
                self.Ingame_settings.update()
            else:
                self.ingame_menu.display()
        else:
            self.input()
            self.level.run()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.pause_game()

        if keys[pygame.K_n]:
            if not self.is_talent_menu_open:
                self.level.toggle_menu(menuenums.TALENTS)
                self.talent_menu_open_time = pygame.time.get_ticks()
                self.is_talent_menu_open = True

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if self.is_talent_menu_open:
            if current_time - self.talent_menu_open_time > self.key_press_cooldown:
                self.is_talent_menu_open = False

    def save_game(self):
        print("gamehandler save")
        self.save.create_save(self.level.player)

    def pause_game(self):
        self.game_paused = not self.game_paused

    def open_ingame_settings(self):
        self.is_settings_menu_open = not self.is_settings_menu_open
