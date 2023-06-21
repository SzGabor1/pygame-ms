import pygame
import sys
from settings import *


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.init_main_menu()

    def init_main_menu(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            self.game.settings.UI_FONT, self.game.settings.UI_FONT_SIZE)

        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (self.game.settings.WIDTH, self.game.settings.HEIGHT))

        self.title_label = self.font.render(
            "Marooned Sailor", True, self.game.settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 2 - 100))

        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 400
        menu_x = (self.game.settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (self.game.settings.HEIGHT - menu_height) // 2

        self.menu_rect = pygame.Rect(
            menu_x, menu_y+50, menu_width, menu_height)

        self.new_game_button = pygame.Rect(
            menu_x + 50, menu_y + 150, 300, 50)
        self.new_game_label = self.font.render(
            "New Game", True, self.game.settings.BLACK_TEXT_COLOR)
        self.new_game_rect = self.new_game_label.get_rect(
            center=self.new_game_button.center)

        self.load_game_button = pygame.Rect(
            menu_x + 50, menu_y + 250, 300, 50)
        self.load_game_label = self.font.render(
            "Load Game", True, self.game.settings.BLACK_TEXT_COLOR)
        self.load_game_rect = self.load_game_label.get_rect(
            center=self.load_game_button.center)

        self.settings_button = pygame.Rect(
            menu_x + 50, menu_y + 350, 300, 50)
        self.settings_label = self.font.render(
            "Settings", True, self.game.settings.BLACK_TEXT_COLOR)
        self.settings_rect = self.settings_label.get_rect(
            center=self.settings_button.center)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.new_game_button.collidepoint(event.pos):
                        print("New Game button clicked!")
                        # Perform action for new game
                    elif self.load_game_button.collidepoint(event.pos):
                        print("Load Game button clicked!")
                        # Perform action for load game
                        self.game.state = "GAME"  # Set the state to "GAME"
                    elif self.settings_button.collidepoint(event.pos):
                        print("Settings button clicked!")
                        # Open settings menu
                        self.game.open_settings_menu()

    def render(self):
        # Fill the screen with the menu background image
        self.screen.blit(self.menu_bg, (0, 0))

        # Draw the menu background rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            self.game.settings.MENU_BG_COLOR), self.menu_rect)

        # Draw the border around the menu rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            self.game.settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        # Draw the menu elements on top of the rectangle
        self.screen.blit(self.title_label, self.title_rect)
        pygame.draw.rect(self.screen, self.game.settings.MENU_BUTTON_BG_COLOR,
                         self.new_game_button)
        self.screen.blit(self.new_game_label, self.new_game_rect)
        pygame.draw.rect(self.screen, self.game.settings.MENU_BUTTON_BG_COLOR,
                         self.load_game_button)
        self.screen.blit(self.load_game_label, self.load_game_rect)
        pygame.draw.rect(self.screen, self.game.settings.MENU_BUTTON_BG_COLOR,
                         self.settings_button)
        self.screen.blit(self.settings_label, self.settings_rect)

        pygame.display.flip()
        self.clock.tick(self.game.settings.FPS)


class SettingsMenu:
    def __init__(self, game):

        self.game = game
        self.init_settings_menu()

    def init_settings_menu(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            self.game.settings.UI_FONT, self.game.settings.UI_FONT_SIZE)
        self.resolution_labels = []
        self.resolution_rects = []
        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (self.game.settings.WIDTH, self.game.settings.HEIGHT))

        self.title_label = self.font.render(
            "Settings", True, self.game.settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 2 - 200))

        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 400
        menu_x = (self.game.settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (self.game.settings.HEIGHT - menu_height) // 2

        self.menu_rect = pygame.Rect(
            menu_x, menu_y - 25, menu_width, menu_height)

        self.save_button = pygame.Rect(
            menu_x + 100, menu_y + 300, 200, 50)
        self.save_label = self.font.render(
            "Save Settings", True, self.game.settings.BLACK_TEXT_COLOR)
        self.save_rect = self.save_label.get_rect(
            center=self.save_button.center)

        for i, resolution in enumerate(self.game.settings.RESOLUTIONS):
            label = self.font.render(
                f"{resolution[0]} x {resolution[1]}", True, self.game.settings.BLACK_TEXT_COLOR)
            rect = label.get_rect(
                center=(self.game.settings.WIDTH // 2, menu_y + 100 + 50 * i))
            self.resolution_labels.append(label)
            self.resolution_rects.append(rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(self.resolution_rects):
                        if rect.collidepoint(event.pos):
                            self.selected_resolution = self.game.settings.RESOLUTIONS[i]
                            break

                    if self.save_button.collidepoint(event.pos):
                        print("Save Settings button clicked!")
                        if hasattr(self, 'selected_resolution'):
                            if self.selected_resolution is not None:
                                print("Selected resolution:",
                                      self.selected_resolution)
                                width, height = self.selected_resolution
                                self.game.settings.overwite_settings(
                                    width, height)
                        self.game.menu.init_main_menu()
                        self.init_settings_menu()
                        self.game.screen = pygame.display.set_mode(
                            (width, height), flags=pygame.RESIZABLE, vsync=1)
                        self.game.state = 'MENU'
                        # Call the game's save_settings method or perform any other necessary actions

    def render(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.menu_bg, (0, 0))

        # Draw the menu background rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            self.game.settings.MENU_BG_COLOR), self.menu_rect)

        # Draw the border around the menu rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            self.game.settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.screen.blit(self.title_label, self.title_rect)
        for i, label in enumerate(self.resolution_labels):
            self.screen.blit(label, self.resolution_rects[i])
        pygame.draw.rect(
            self.screen, self.game.settings.MENU_BUTTON_BG_COLOR, self.save_button)
        self.screen.blit(self.save_label, self.save_rect)
        pygame.display.flip()
        self.clock.tick(self.game.settings.FPS)
