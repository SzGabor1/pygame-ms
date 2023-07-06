import pygame
from pygame.locals import *
import sys
from settings import Settings
from support import import_settings
from mainmenu import MainMenu, SettingsMenu, NewGameMenu, LoadMenu
from menuenums import menuenums
from gamehandler import GameHandler
from save import Save


class Game:

    def __init__(self):
        self.settings = Settings(
            import_settings('data/settings/settings.json'))
        pygame.init()
        self.init_screen()
        pygame.display.set_caption("Marooned Sailor")
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(self)
        self.game_handler = None
        self.settings_menu = None
        self.load_menu = None
        self.new_game_menu = None
        self.state = menuenums.MENU
        self.mapGenerated = False
        self.save_parameters = None

    def init_screen(self):
        if self.settings.FULLSCREEN:
            self.screen = pygame.display.set_mode(
                (self.settings.WIDTH, self.settings.HEIGHT), flags=pygame.FULLSCREEN | pygame.SCALED, vsync=1)
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.WIDTH, self.settings.HEIGHT), flags=pygame.RESIZABLE | pygame.SCALED, vsync=1)

    def run(self):
        while True:
            if self.state == menuenums.MENU:
                self.menu.update()
                self.menu.render()
            elif self.state == menuenums.SETTINGS:
                if self.settings_menu is not None:
                    self.settings_menu.update()
                    self.settings_menu.render()
            if self.state == menuenums.LOAD_GAME:
                self.load_menu.update()
                self.load_menu.render()
            elif self.state == menuenums.NEW_GAME_MENU:
                self.new_game_menu.update()
                self.new_game_menu.render()
            elif self.state == menuenums.GAME:
                if self.game_handler is None:
                    self.game_handler = GameHandler(
                        self.settings, self.save_parameters)
                    self.mapGenerated = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_n:
                            self.game_handler.level.toggle_menu(
                                menuenums.TALENTS)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game_handler.pause_game()
                self.screen.fill(self.settings.WATER_COLOR)
                self.game_handler.run()
                pygame.display.update()
                self.clock.tick(self.settings.FPS)

    def open_new_game_menu(self):
        self.new_game_menu = NewGameMenu(self)
        self.state = menuenums.NEW_GAME_MENU

    def open_load_menu(self):
        self.load_menu = LoadMenu(self)
        self.state = menuenums.LOAD_GAME

    def open_settings_menu(self):
        self.settings_menu = SettingsMenu(self)
        self.state = menuenums.SETTINGS


if __name__ == '__main__':
    game = Game()
    game.run()
