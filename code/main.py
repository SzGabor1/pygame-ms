import pygame
from pygame.locals import *
import sys
from settings import Settings
from support import import_settings
from level import Level
from mainmenu import MainMenu, SettingsMenu


class Game:

    def __init__(self):
        self.settings = Settings(
            import_settings('data/settings/settings.json'))
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.settings.WIDTH, self.settings.HEIGHT), flags=pygame.RESIZABLE)
        pygame.display.set_caption("Marooned Sailor")
        self.clock = pygame.time.Clock()
        self.level = Level(self.settings)
        self.menu = MainMenu(self)
        self.settings_menu = None
        self.state = 'MENU'

    def run(self):
        while True:
            if self.state == 'MENU':
                self.menu.update()
                self.menu.render()
            elif self.state == 'SETTINGS':
                if self.settings_menu is not None:
                    self.settings_menu.update()
                    self.settings_menu.render()
            elif self.state == 'GAME':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_n:
                            self.level.toggle_menu('talents')
                self.screen.fill(self.settings.WATER_COLOR)
                self.level.run()
                pygame.display.update()
                self.clock.tick(self.settings.FPS)

    def start_new_game(self):
        # Logic for starting a new game
        # Reset player data, initialize a new Level instance, etc.
        pass

    def load_game(self):
        # Logic for loading a saved game
        # Load player data, initialize a Level instance with the loaded data, etc.
        pass

    def open_settings_menu(self):
        self.settings_menu = SettingsMenu(self)
        self.state = 'SETTINGS'


if __name__ == '__main__':
    game = Game()
    game.run()
