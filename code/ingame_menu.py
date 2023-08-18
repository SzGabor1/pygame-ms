import sys
import pygame
from mainmenu import SettingsMenu
from sound import Sounds
from settings import Settings
import game_api_client


class IngameMenu:
    def __init__(self, pause_game, save_game, open_ingame_settings):
        self.display_surface = pygame.display.get_surface()
        self.pause_game = pause_game
        self.open_ingame_settings = open_ingame_settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))

        self.menu_items = ["Resume", "Save", "Settings", "Exit"]
        self.menu_item_height = self.font.get_height() + 10
        self.menu_width = 400
        self.menu_height = len(self.menu_items) * self.menu_item_height + 20
        self.menu_x = (Settings.WIDTH - self.menu_width) // 2
        self.menu_y = (Settings.HEIGHT - self.menu_height) // 2 + 50
        self.menu_rect = pygame.Rect(
            self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        self.menu_items_rects = []
        self.selected_item = 0

        self.cooldown_time = 500  # milliseconds
        self.last_click_time = 0

        self.save_game = save_game
        self.is_game_saved = True
        self.save_time = None

    def display(self):
        self.update()
        self.render()

    def show_game_saved(self):
        if not self.is_game_saved:
            text_surf = self.font.render(
                "Game saved!", True, Settings.BLACK_TEXT_COLOR)
            text_rect = text_surf.get_rect(center=(
                Settings.WIDTH // 2, Settings.HEIGHT // 2-250))
            self.display_surface.blit(text_surf, text_rect)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.is_game_saved:
            if current_time - self.save_time >= self.cooldown_time:
                self.is_game_saved = True

    def update(self):
        self.cooldown()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        if mouse_clicked and current_time - self.last_click_time > self.cooldown_time:
            self.handle_menu_selection(mouse_pos)
            self.last_click_time = current_time

    def handle_menu_selection(self, mouse_pos):
        for index, rect in enumerate(self.menu_items_rects):
            if rect.collidepoint(mouse_pos):
                if 0 <= index < len(self.menu_items):
                    selected_item = self.menu_items[index]
                    if selected_item == "Resume":
                        print("Resume button clicked!")
                        self.pause_game()
                        # Resume the game
                    elif selected_item == "Save":
                        print("Save button clicked!")
                        self.save_game()
                        self.save_time = pygame.time.get_ticks()
                        self.is_game_saved = False
                        # Save the game
                    elif selected_item == "Settings":
                        print("Settings button clicked!")
                        self.open_ingame_settings()
                    elif selected_item == "Exit":
                        print("Exit button clicked!")
                        pygame.quit()
                        sys.exit()

    def render(self):
        self.display_surface.blit(self.menu_bg, (0, 0))

        pygame.draw.rect(self.display_surface, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)
        pygame.draw.rect(self.display_surface, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.menu_items_rects = []  # Clear the previous menu item rectangles

        for index, item in enumerate(self.menu_items):
            item_surf = self.font.render(
                item, True, Settings.BLACK_TEXT_COLOR)
            item_rect = item_surf.get_rect(center=(
                self.menu_rect.centerx, self.menu_rect.top + self.menu_item_height * index + self.menu_item_height // 2))
            self.menu_items_rects.append(item_rect)
            self.display_surface.blit(item_surf, item_rect)

        self.show_game_saved()

        pygame.display.flip()
        self.clock.tick(Settings.FPS)


class Ingame_settings():
    def __init__(self, open_ingame_settings):
        self.open_ingame_settings = open_ingame_settings
        self.init_settings_menu()

    def init_settings_menu(self):

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)
        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))
        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 500
        menu_x = (Settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (Settings.HEIGHT - menu_height) // 2
        self.menu_rect = pygame.Rect(
            menu_x, menu_y - 25, menu_width, menu_height)

        self.save_button = pygame.Rect(
            menu_x + 100, menu_y + 400, 200, 50)
        self.save_label = self.font.render(
            "Save", True, Settings.BLACK_TEXT_COLOR)
        self.save_rect = self.save_label.get_rect(
            center=self.save_button.center)
        self.title_label = self.font.render(
            "Settings", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))
        self.volume_label = self.font.render(
            "Volume:", True, Settings.BLACK_TEXT_COLOR)
        self.volume_rect = self.volume_label.get_rect(
            center=(Settings.WIDTH // 2, menu_y + 250))
        self.volume_slider = pygame.Rect(
            menu_x + 100, menu_y + 280, 200, 20)
        self.volume_slider_handle = pygame.Rect(
            menu_x + 100, menu_y + 275, 10, 30)
        self.volume_min = 0
        self.volume_max = 100
        self.current_volume = Settings.VOLUME * 100

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.volume_slider.collidepoint(event.pos):
                        mouse_x, _ = event.pos
                        relative_x = mouse_x - self.volume_slider.x
                        self.current_volume = int(
                            relative_x / self.volume_slider.width * (self.volume_max - self.volume_min))
                        self.current_volume = min(
                            max(self.current_volume, self.volume_min), self.volume_max)

                    if self.save_button.collidepoint(event.pos):
                        print("Save button clicked!")
                        Settings.overwrite_volume(self.current_volume/100)
                        Sounds.set_static_volume(self.current_volume/100)
                        self.open_ingame_settings()

    def render(self):

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.menu_bg, (0, 0))
        # Draw the menu background rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)

        # Draw the border around the menu rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.screen.blit(self.title_label, self.title_rect)
        # Draw the volume label and slider
        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.volume_slider)
        pygame.draw.rect(
            self.screen, Settings.MENU_BORDER_COLOR, self.volume_slider, 2)
        self.volume_slider_handle.centerx = self.volume_slider.left + int(
            self.volume_slider.width * (self.current_volume / self.volume_max))
        pygame.draw.rect(
            self.screen, Settings.BLACK_TEXT_COLOR, self.volume_slider_handle)

        self.screen.blit(self.volume_label, self.volume_rect)

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.save_button)
        self.screen.blit(self.save_label, self.save_rect)

        pygame.display.flip()
        self.clock.tick(Settings.FPS)


class HowToPlay():
    def __init__(self, open_how_to_play):
        self.open_how_to_play = open_how_to_play
        self.init_how_to_play()

    def init_how_to_play(self):

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        menu_width = 500
        menu_height = 600
        menu_x = (Settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (Settings.HEIGHT - menu_height) // 2
        self.menu_rect = pygame.Rect(
            menu_x, menu_y - 25, menu_width, menu_height)

        self.back_button = pygame.Rect(
            menu_x + 150, menu_y + 400, 200, 50)
        self.back_label = self.font.render(
            "Back", True, Settings.BLACK_TEXT_COLOR)
        self.save_rect = self.back_label.get_rect(
            center=self.back_button.center)
        self.title_label = self.font.render(
            "How to play", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))

        self.instructions = [
            "WASD - Movement",
            "E - Switch weapon.",
            "E - interact with NPCs, dungeon.",
            "M - Map",
            "N - Stats",
            "Space - Upgrade Stat",
            "Q - Use Potion",
        ]

    def display(self):
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        print("Save button clicked!")
                        self.open_how_to_play()

    def render(self):

        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)

        # Draw the border around the menu rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.screen.blit(self.title_label, self.title_rect)

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.back_button)
        self.screen.blit(self.back_label, self.save_rect)

        y_offset = self.title_rect.bottom + 20
        line_height = 30

        for instruction in self.instructions:
            instruction_label = self.font.render(
                instruction, True, Settings.BLACK_TEXT_COLOR)
            instruction_rect = instruction_label.get_rect(
                center=(self.menu_rect.centerx, y_offset))
            self.screen.blit(instruction_label, instruction_rect)
            y_offset += line_height


class Leaderboard:
    def __init__(self, open_leaderboard):
        self.open_leaderboard = open_leaderboard
        self.init_leaderboard()

    def init_leaderboard(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        menu_width = 500
        menu_height = 600
        menu_x = (Settings.WIDTH - menu_width) // 2
        menu_y = (Settings.HEIGHT - menu_height) // 2
        self.menu_rect = pygame.Rect(
            menu_x, menu_y - 25, menu_width, menu_height)

        self.back_button = pygame.Rect(
            menu_x + 150, menu_y + 400, 200, 50)
        self.back_label = self.font.render(
            "Back", True, Settings.BLACK_TEXT_COLOR)
        self.back_rect = self.back_label.get_rect(
            center=self.back_button.center)
        self.title_label = self.font.render(
            "Leaderboard", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))

        self.top_players = game_api_client.get_top_ten_highest_level_users()

    def display(self):
        self.update()
        self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        print("Back button clicked!")
                        self.open_leaderboard()

    def render(self):
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.screen.blit(self.title_label, self.title_rect)

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.back_button)
        self.screen.blit(self.back_label, self.back_rect)

        y_offset = self.title_rect.bottom + 20
        line_height = 30

        for player_data in self.top_players:
            player_label = self.font.render(
                f"{player_data['username']} - Level {player_data['highest_level']}",
                True, Settings.BLACK_TEXT_COLOR
            )
            player_rect = player_label.get_rect(
                center=(self.menu_rect.centerx, y_offset))
            self.screen.blit(player_label, player_rect)
            y_offset += line_height
