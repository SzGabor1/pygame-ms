import pygame

from level import Level
from save import Save
from ingame_menu import IngameMenu, Ingame_settings
from menuenums import menuenums
from settings import Settings


class GameHandler():
    def __init__(self, user, what_to_load):
        self.user = user
        if self.user is not None:
            self.save = Save(what_to_load, self.user.characters)
        else:
            self.save = Save(what_to_load, None)
        self.game_paused = False
        self.level = Level(self.save.load_data())
        self.ingame_menu = IngameMenu(
            self.pause_game, self.save_game, self.open_ingame_settings)

        self.is_settings_menu_open = False
        self.Ingame_settings = Ingame_settings(self.open_ingame_settings)

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

        if self.user is not None:
            self.save.create_online_save(
                self.level.player, self.save.load_data()[1]['id'], self.user.id)
        else:
            self.save.create_save(self.level.player)

    def pause_game(self):
        self.game_paused = not self.game_paused

    def open_ingame_settings(self):
        self.is_settings_menu_open = not self.is_settings_menu_open
