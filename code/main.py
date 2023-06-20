import pygame
import sys
from settings import *
from level import Level
from mainmenu import MainMenu, SettingsMenu
from temp import tempsettings


class Game:
    def __init__(self):
        self.check_new_settings()
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)
        pygame.display.set_caption("Marooned Sailor")
        self.clock = pygame.time.Clock()
        self.level = Level()
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
                self.screen.fill(WATER_COLOR)
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

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

    def check_new_settings(self):
        if WIDTH != tempsettings.WIDTH or HEIGHT != tempsettings.HEIGHT:
            with open("code/settings.py", "r") as config_file:
                lines = config_file.readlines()

            if lines[0].startswith("WIDTH =") and lines[1].startswith("HEIGHT ="):
                if WIDTH != tempsettings.WIDTH or HEIGHT != tempsettings.HEIGHT:
                    lines[0] = f"WIDTH = {tempsettings.WIDTH}\n"
                    lines[1] = f"HEIGHT = {tempsettings.HEIGHT}\n"

            with open("code/settings.py", "w") as config_file:
                config_file.writelines(lines)


if __name__ == '__main__':
    game = Game()
    game.run()
