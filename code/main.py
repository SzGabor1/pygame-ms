import pygame
from pygame.locals import *
import sys
from settings import Settings
from mainmenu import MainMenu, SettingsMenu, NewGameMenu, LoadMenu, CreditsMenu
from menuenums import menuenums
from gamehandler import GameHandler
from sound import Sounds
from user_auth import LoginPanel


class Game:
    def __init__(self):

        self.user = None
        self.online = False

        pygame.init()
        self.init_screen()
        pygame.display.set_caption("Marooned Sailor")
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(self)
        self.game_handler = None
        self.settings_menu = None
        # self.load_menu = None
        # self.new_game_menu = None
        self.state = menuenums.LOGIN
        # self.mapGenerated = False
        self.save_parameters = None
        self.login_panel = LoginPanel(self)

    def init_screen(self):
        self.screen = pygame.display.set_mode(
            (Settings.WIDTH, Settings.HEIGHT), flags=pygame.FULLSCREEN | pygame.SCALED, vsync=1)

    def run(self):

        while True:
            if self.state == menuenums.LOGIN:
                self.login_panel.update()
                self.login_panel.render()

            if self.state == menuenums.MENU:
                self.menu.update()
                self.menu.render()
            elif self.state == menuenums.SETTINGS:

                if self.settings_menu is not None:
                    self.settings_menu.update()
                    self.settings_menu.render()
                    self.clock.tick(Settings.FPS)
            elif self.state == menuenums.CREDITS:
                self.credits_menu = CreditsMenu(self)
                self.credits_menu.update()
                self.credits_menu.render()

            if self.state == menuenums.LOAD_GAME:

                self.load_menu.update()
                self.load_menu.render()
            elif self.state == menuenums.NEW_GAME_MENU:

                self.new_game_menu.update()
                self.new_game_menu.render()
            elif self.state == menuenums.GAME:
                if self.game_handler is None:
                    Sounds.play_loop('main')
                    self.game_handler = GameHandler(
                        self.user, self.save_parameters)
                    # self.mapGenerated = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                self.screen.fill(Settings.WATER_COLOR)
                self.game_handler.run()
                pygame.display.update()
                self.clock.tick(Settings.FPS)

    def open_new_game_menu(self):
        Sounds.play('click')
        self.new_game_menu = NewGameMenu(self)
        self.state = menuenums.NEW_GAME_MENU

    def open_load_menu(self):
        Sounds.play('click')
        if self.online:
            self.load_menu = LoadMenu(self, self.user.characters)
        else:
            self.load_menu = LoadMenu(self, None)
        self.state = menuenums.LOAD_GAME

    def open_settings_menu(self):
        Sounds.play('click')
        self.settings_menu = SettingsMenu(self)
        self.state = menuenums.SETTINGS


if __name__ == '__main__':
    game = Game()
    game.run()
