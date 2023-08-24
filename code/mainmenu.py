import pygame
import sys
from settings import *
from menuenums import menuenums
from support import import_character_profile_images
from save import get_save_files
from screeninfo import get_monitors
from settings import Settings


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.init_main_menu()

    def init_main_menu(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))

        self.title_label = self.font.render(
            "Marooned Sailor", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 100))

        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 400
        menu_x = (Settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (Settings.HEIGHT - menu_height) // 2

        self.menu_rect = pygame.Rect(
            menu_x, menu_y+50, menu_width, menu_height)

        self.new_game_button = pygame.Rect(
            menu_x + 50, menu_y + 150, 300, 50)
        self.new_game_label = self.font.render(
            "New Game", True, Settings.BLACK_TEXT_COLOR)
        self.new_game_rect = self.new_game_label.get_rect(
            center=self.new_game_button.center)

        self.load_game_button = pygame.Rect(
            menu_x + 50, menu_y + 250, 300, 50)
        self.load_game_label = self.font.render(
            "Load Game", True, Settings.BLACK_TEXT_COLOR)
        self.load_game_rect = self.load_game_label.get_rect(
            center=self.load_game_button.center)

        self.settings_button = pygame.Rect(
            menu_x + 50, menu_y + 350, 300, 50)
        self.settings_label = self.font.render(
            "Settings", True, Settings.BLACK_TEXT_COLOR)
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
                        self.game.open_new_game_menu()
                        # Perform action for new game
                    elif self.load_game_button.collidepoint(event.pos):
                        print("Load Game button clicked!")
                        # Perform action for load game
                        self.game.open_load_menu()  # Set the state to "GAME"
                    elif self.settings_button.collidepoint(event.pos):
                        print("Settings button clicked!")
                        # Open settings menu
                        self.game.open_settings_menu()

    def render(self):
        # Fill the screen with the menu background image
        self.screen.blit(self.menu_bg, (0, 0))

        # Draw the menu background rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)

        # Draw the border around the menu rectangle
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        # Draw the menu elements on top of the rectangle
        self.screen.blit(self.title_label, self.title_rect)
        pygame.draw.rect(self.screen, Settings.MENU_BUTTON_BG_COLOR,
                         self.new_game_button)
        self.screen.blit(self.new_game_label, self.new_game_rect)
        pygame.draw.rect(self.screen, Settings.MENU_BUTTON_BG_COLOR,
                         self.load_game_button)
        self.screen.blit(self.load_game_label, self.load_game_rect)
        pygame.draw.rect(self.screen, Settings.MENU_BUTTON_BG_COLOR,
                         self.settings_button)
        self.screen.blit(self.settings_label, self.settings_rect)

        pygame.display.flip()
        # self.clock.tick(Settings.FPS)


class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.init_settings_menu()

    def init_settings_menu(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))

        self.title_label = self.font.render(
            "Settings", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))

        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 500
        menu_x = (Settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (Settings.HEIGHT - menu_height) // 2

        self.menu_rect = pygame.Rect(
            menu_x, menu_y - 25, menu_width, menu_height)

        self.save_button = pygame.Rect(
            menu_x + 100, menu_y + 200, 200, 50)
        self.save_label = self.font.render(
            "Save Settings", True, Settings.BLACK_TEXT_COLOR)
        self.save_rect = self.save_label.get_rect(
            center=self.save_button.center)

        self.fullscreen = Settings.FULLSCREEN
        # Create the fullscreen label
        self.fullscreen_label = self.font.render(
            "Fullscreen:", True, Settings.BLACK_TEXT_COLOR)
        self.fullscreen_rect = self.fullscreen_label.get_rect(
            center=(Settings.WIDTH // 2, menu_y + 100))

        # Create the "yes" and "no" text labels
        self.fullscreen_option_labels = [
            self.font.render("Yes", True, Settings.BLACK_TEXT_COLOR),
            self.font.render("No", True, Settings.BLACK_TEXT_COLOR)
        ]

        # Position the "yes" and "no" text labels in line with the fullscreen label
        fullscreen_label_width = self.fullscreen_label.get_width()
        fullscreen_option_spacing = 50
        fullscreen_option_x = self.fullscreen_rect.right + fullscreen_option_spacing
        fullscreen_option_y = self.fullscreen_rect.centery - \
            self.fullscreen_option_labels[0].get_height() // 2
        self.fullscreen_option_rects = [
            self.fullscreen_option_labels[0].get_rect(
                center=(Settings.WIDTH // 2-70, menu_y + 140)),
            self.fullscreen_option_labels[1].get_rect(
                center=(Settings.WIDTH // 2+70, menu_y + 140))
        ]

        self.credits_button = pygame.Rect(
            (Settings.WIDTH - 200) // 2, self.menu_rect.centery + 100, 200, 50)
        self.credits_label = self.font.render(
            "Credits", True, Settings.BLACK_TEXT_COLOR)
        self.credits_rect = self.credits_label.get_rect(
            center=self.credits_button.center)

    def update(self):
        self.clock.tick(Settings.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check for fullscreen label selection
                    for i, rect in enumerate(self.fullscreen_option_rects):
                        if rect.collidepoint(event.pos):
                            self.fullscreen = i == 0  # 0 represents "Yes", 1 represents "No"
                            break

                        if self.credits_button.collidepoint(event.pos):
                            print("Credits button clicked!")
                            self.game.state = menuenums.CREDITS

                    if self.save_button.collidepoint(event.pos):
                        print("Save Settings button clicked!")
                        # Get the primary monitor
                        monitor = get_monitors()[0]

                        # Retrieve the width and height of the monitor
                        width = monitor.width
                        height = monitor.height

                        print("Monitor size: {}x{}".format(width, height))
                        if self.fullscreen:
                            Settings.overwrite_settings(
                                width, height, fullscreen=self.fullscreen,  volume=None)

                            self.game.init_screen()
                            self.game.menu.init_main_menu()
                            self.init_settings_menu()
                            self.game.screen = pygame.display.set_mode(
                                (width, height), flags=pygame.FULLSCREEN if self.fullscreen else 0, vsync=1)

                        else:
                            height = height - 50
                            Settings.overwrite_settings(
                                width, height, fullscreen=self.fullscreen, volume=None)

                            self.game.init_screen()
                            self.game.menu.init_main_menu()
                            self.init_settings_menu()
                            self.game.screen = pygame.display.set_mode(
                                (width, height), flags=pygame.RESIZABLE if not self.fullscreen else 0, vsync=1)

                        self.game.state = menuenums.MENU

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

        # Draw the "Credits" button
        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.credits_button)
        self.screen.blit(self.credits_label, self.credits_rect)

        # Draw the fullscreen label
        self.screen.blit(self.fullscreen_label, self.fullscreen_rect)

        # Draw the "yes" and "no" text labels
        for i, label in enumerate(self.fullscreen_option_labels):
            rect = self.fullscreen_option_rects[i]
            if self.fullscreen and i == 0:
                text_color = Settings.MENU_BUTTON_BG_COLOR
            elif not self.fullscreen and i == 1:
                text_color = Settings.MENU_BUTTON_BG_COLOR
            else:
                text_color = Settings.MENU_BG_COLOR

            # Highlight the selected fullscreen option
            pygame.draw.rect(self.screen, text_color, rect)
            self.screen.blit(label, rect)

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.save_button)
        self.screen.blit(self.save_label, self.save_rect)
        pygame.display.flip()
        # self.clock.tick(Settings.FPS)


class NewGameMenu:
    def __init__(self, game):
        self.game = game
        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))
        self.character_name = ""
        self.character_image = None
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        self.button_state = 0
        # Calculate the dimensions of the button based on the text size
        button_text = "Challenge Mode"  # Longer text to determine dimensions
        self.button_width = self.font.size(button_text)[0] + 10
        self.button_height = self.font.size(button_text)[1] + 10

        self.button_rect = pygame.Rect(
            Settings.WIDTH // 2 - self.button_width // 2,
            Settings.HEIGHT // 2 + 100 - self.button_height // 2,
            self.button_width, self.button_height)

        self.title_label = self.font.render(
            "Create New Game", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))

        self.menu_width = 500
        self.menu_height = 500
        self.menu_x = (Settings.WIDTH - self.menu_width) // 2
        self.menu_y = (Settings.HEIGHT - self.menu_height) // 2 - 100

        self.menu_rect = pygame.Rect(
            self.menu_x, self.menu_y + 100, self.menu_width, self.menu_height)

        self.name_label = self.font.render(
            "Enter Character Name:", True, Settings.BLACK_TEXT_COLOR)
        self.name_rect = self.name_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 150))

        self.name_input_rect = pygame.Rect(
            Settings.WIDTH // 2 - 100, Settings.HEIGHT // 2 - 130, 200, 30)

        self.image_label = self.font.render(
            "Choose Character Image:", True, Settings.BLACK_TEXT_COLOR)
        self.image_rect = self.image_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 50))

        self.save_button = pygame.Rect(
            Settings.WIDTH // 2 - 100, Settings.HEIGHT // 2 + 150, 80, 30)
        self.save_label = self.font.render(
            "Save", True, Settings.BLACK_TEXT_COLOR)
        self.save_rect = self.save_label.get_rect(
            center=self.save_button.center)

        self.back_button = pygame.Rect(
            Settings.WIDTH // 2 + 20, Settings.HEIGHT // 2 + 150, 80, 30)
        self.back_label = self.font.render(
            "Back", True, Settings.BLACK_TEXT_COLOR)
        self.back_rect = self.back_label.get_rect(
            center=self.back_button.center)

        self.character_images = import_character_profile_images()

        self.current_character_index = 0
        self.current_character_image = self.character_images[self.current_character_index]

        # Triangle dimensions
        self.triangle_size = 20

        # Triangle coordinates for left and right
        self.triangle_left_x = self.menu_x + 70 + self.triangle_size // 2
        self.triangle_left_y = self.menu_y + \
            self.menu_height // 2 + 150 + self.triangle_size // 2

        self.triangle_right_x = self.menu_x + \
            self.menu_width - 70 - self.triangle_size // 2
        self.triangle_right_y = self.menu_y + \
            self.menu_height // 2 + 150 + self.triangle_size // 2

        self.left_rectangle = pygame.Rect(
            self.menu_x + 70, self.menu_y + self.menu_height // 2 + 150, self.triangle_size, self.triangle_size)

        self.right_rectangle = pygame.Rect(
            self.menu_x + self.menu_width - 70 - self.triangle_size, self.menu_y + self.menu_height // 2 + 150, self.triangle_size, self.triangle_size)

    def render(self):
        self.screen.blit(self.menu_bg, (0, 0))
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)
        self.screen.blit(self.title_label, self.title_rect)
        self.screen.blit(self.name_label, self.name_rect)

        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.name_input_rect)
        name_input_text = self.font.render(
            self.character_name, True, Settings.BLACK_TEXT_COLOR)
        self.screen.blit(name_input_text, self.name_input_rect.move(5, 5))

        self.screen.blit(self.image_label, self.image_rect)

        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.save_button)
        self.screen.blit(self.save_label, self.save_rect)

        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.back_button)
        self.screen.blit(self.back_label, self.back_rect)

        # Draw the character image
        character_image_rect = self.current_character_image.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 50))
        self.screen.blit(self.current_character_image, character_image_rect)

        # Draw the rectangles
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.left_rectangle)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.right_rectangle)

        # Calculate the triangle positions
        left_triangle_x = self.triangle_left_x + 20 - self.triangle_size // 2
        left_triangle_y = self.triangle_left_y

        right_triangle_x = self.triangle_right_x - self.triangle_size // 2
        right_triangle_y = self.triangle_right_y

        # Draw the left arrow triangle
        pygame.draw.polygon(self.screen, pygame.Color(Settings.BLACK_TEXT_COLOR), [
            (left_triangle_x, left_triangle_y - self.triangle_size // 2),
            (left_triangle_x - self.triangle_size, left_triangle_y),
            (left_triangle_x, left_triangle_y + self.triangle_size // 2)
        ])

        # Draw the right arrow triangle
        pygame.draw.polygon(self.screen, pygame.Color(Settings.BLACK_TEXT_COLOR), [
            (right_triangle_x, right_triangle_y - self.triangle_size // 2),
            (right_triangle_x + self.triangle_size, right_triangle_y),
            (right_triangle_x, right_triangle_y + self.triangle_size // 2)
        ])

        if self.button_state == 0:
            button_label = self.font.render(
                "Normal Mode", True, Settings.BLACK_TEXT_COLOR)
        else:
            button_label = self.font.render(
                "Challenge Mode", True, Settings.BLACK_TEXT_COLOR)

        # Update the button dimensions based on the text size
        self.button_width = button_label.get_width() + 10
        self.button_height = button_label.get_height() + 10
        self.button_rect.width = self.button_width
        self.button_rect.height = self.button_height

        # Adjust the text position to center it vertically
        button_label_rect = button_label.get_rect(
            center=self.button_rect.center)

        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.button_rect)
        self.screen.blit(button_label, button_label_rect.topleft)

        pygame.display.flip()
        # self.clock.tick(Settings.FPS)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if the save button is clicked
                    if self.save_button.collidepoint(mouse_pos):
                        print("Save button clicked!")
                        if self.game.online:

                            for character in self.game.user.characters:
                                if character.player_name == self.character_name:
                                    print("Character name already exists!")
                                    return

                            self.game.save_parameters = ("new_online",
                                                         self.character_name, self.current_character_index, self.button_state, self.game.user.id)
                        else:
                            self.game.save_parameters = ("new",
                                                         self.character_name, self.current_character_index, self.button_state)
                        self.game.state = menuenums.GAME

                    # Check if the back button is clicked
                    elif self.back_button.collidepoint(mouse_pos):
                        print("Back button clicked!")
                        self.game.state = menuenums.MENU

                    # Check if the left rectangle is clicked
                    elif self.left_rectangle.collidepoint(mouse_pos):
                        print("Left rectangle clicked!")
                        self.current_character_index -= 1
                        if self.current_character_index < 0:
                            self.current_character_index = len(
                                self.character_images) - 1
                        self.current_character_image = self.character_images[self.current_character_index]

                    # Check if the right rectangle is clicked
                    elif self.right_rectangle.collidepoint(mouse_pos):
                        print("Right rectangle clicked!")
                        self.current_character_index += 1
                        if self.current_character_index >= len(self.character_images):
                            self.current_character_index = 0
                        self.current_character_image = self.character_images[self.current_character_index]

                    elif self.button_rect.collidepoint(mouse_pos) and self.game.online:
                        print("Button clicked!")
                        self.button_state = 1 - self.button_state  # Toggle between 0 and 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the character name
                    self.character_name = self.character_name[:-1]
                else:
                    # Add the pressed character to the character name
                    self.character_name += event.unicode

        self.render()


class LoadMenu:
    def __init__(self, game, online_characters):
        self.game = game
        self.online_characters = online_characters
        self.init_load_menu()

    def init_load_menu(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))

        self.title_label = self.font.render(
            "Load Game", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))

        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 500
        menu_x = (Settings.WIDTH - menu_width) // 2
        menu_y = (Settings.HEIGHT - menu_height) // 2

        self.menu_rect = pygame.Rect(
            menu_x, menu_y - 25, menu_width, menu_height)

        self.back_button = pygame.Rect(
            menu_x + 50, menu_y + 350, 300, 50)
        self.back_label = self.font.render(
            "Back", True, Settings.BLACK_TEXT_COLOR)
        self.back_rect = self.back_label.get_rect(
            center=self.back_button.center)

        self.saves_folder = "saves/"
        self.save_files = get_save_files(self.saves_folder)

        if self.online_characters is not None:
            for character in self.online_characters:
                self.save_files.append(character.player_name)

        self.save_buttons = []

        # Slider változók
        self.slider_rect = pygame.Rect(
            menu_x + 370, menu_y + 100, 20, 200)
        self.slider_button_rect = pygame.Rect(
            menu_x + 360, menu_y + 100, 40, 20)
        self.slider_dragging = False
        self.slider_value = 0
        self.visible_save_files = []
        self.update_visible_save_files()

    def handle_button_click(self, button_index):
        if 0 <= button_index < len(self.visible_save_files):
            selected_button_text = self.visible_save_files[button_index]
            if self.is_online_character(selected_button_text):

                self.game.save_parameters = ("online", selected_button_text)

            else:
                self.game.save_parameters = ("existing", selected_button_text)
            self.game.state = menuenums.GAME

    def is_online_character(self, name):
        if self.online_characters is not None:
            for character in self.online_characters:
                if character.player_name == name:
                    return True
        return False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.back_button.collidepoint(event.pos):
                        print("Back button clicked!")
                        self.game.menu.init_main_menu()
                        self.game.state = menuenums.MENU
                    elif self.slider_button_rect.collidepoint(event.pos):
                        self.slider_dragging = True
                    else:
                        for i, button_rect in enumerate(self.save_buttons):
                            if button_rect.collidepoint(event.pos):
                                self.handle_button_click(i)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.slider_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.slider_dragging:
                    self.slider_button_rect.centery = max(
                        self.slider_rect.top, min(event.pos[1], self.slider_rect.bottom))
                    self.update_slider_value()
                    self.update_visible_save_files()

    def update_slider_value(self):
        slider_range = self.slider_rect.height - self.slider_button_rect.height
        distance_from_top = self.slider_button_rect.centery - self.slider_rect.top
        self.slider_value = distance_from_top / slider_range

    def update_visible_save_files(self):
        num_files = len(self.save_files)

        num_visible_files = min(4, num_files)
        start_index = int(self.slider_value * (num_files - num_visible_files))
        self.visible_save_files = self.save_files[start_index: start_index +
                                                  num_visible_files]

    def render(self):
        self.screen.blit(self.menu_bg, (0, 0))
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)
        self.screen.blit(self.title_label, self.title_rect)

        # Draw the back button
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.back_button)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.back_button, 3)
        self.screen.blit(self.back_label, self.back_rect)

        # Draw the slider
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.slider_rect)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.slider_rect, 3)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BUTTON_BG_COLOR), self.slider_button_rect)

        # Draw save buttons
        self.save_buttons = []
        for i, save_file in enumerate(self.visible_save_files):
            button_rect = pygame.Rect(
                self.menu_rect.left + 50, self.menu_rect.top + 100 + i * 60, self.menu_rect.width - 100, 50)
            self.save_buttons.append(button_rect)
            save_label = self.font.render(
                save_file, True, Settings.BLACK_TEXT_COLOR)
            save_rect = save_label.get_rect(
                left=button_rect.left + 10, centery=button_rect.centery)
            pygame.draw.rect(self.screen, pygame.Color(
                Settings.MENU_BUTTON_BG_COLOR), button_rect)
            pygame.draw.rect(self.screen, pygame.Color(
                Settings.MENU_BORDER_COLOR), button_rect, 3)
            self.screen.blit(save_label, save_rect)

        pygame.display.flip()


class CreditsMenu:
    def __init__(self, game):
        self.game = game
        self.init_credit_menu()

    def init_credit_menu(self):

        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(Settings.UI_FONT, Settings.UI_FONT_SIZE)

        self.title_label = self.font.render(
            "Credits", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))

        self.menu_width = 500
        self.menu_height = 500
        self.menu_x = (Settings.WIDTH - self.menu_width) // 2
        self.menu_y = (Settings.HEIGHT - self.menu_height) // 2 - 100

        self.menu_rect = pygame.Rect(
            self.menu_x, self.menu_y + 100, self.menu_width, self.menu_height)

        self.back_button = pygame.Rect(
            (Settings.WIDTH - 200) // 2, (Settings.HEIGHT + 200) // 2, 200, 50)
        self.back_label = self.font.render(
            "Back", True, Settings.BLACK_TEXT_COLOR)
        self.back_rect = self.back_label.get_rect(
            center=self.back_button.center)

        # Text labels
        self.text_labels = [
            self.font.render("AMtech Rendszerház", True,
                             Settings.BLACK_TEXT_COLOR),
            self.font.render("Készítette:", True,
                             Settings.BLACK_TEXT_COLOR),
            self.font.render("Szendrei Gábor", True,
                             Settings.BLACK_TEXT_COLOR),
            self.font.render("2023", True, Settings.BLACK_TEXT_COLOR)
        ]
        self.text_rects = [
            self.text_labels[0].get_rect(
                center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 100)),
            self.text_labels[1].get_rect(
                center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 50)),
            self.text_labels[2].get_rect(
                center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 0)),
            self.text_labels[3].get_rect(
                center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 50))
        ]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if self.back_button.collidepoint(event.pos):
                        print("Back button clicked!")
                        self.game.state = menuenums.SETTINGS  # Set the game state to SETTINGS
                        # Handle the action you want to take when the "Back" button is clicked

    def render(self):
        self.screen.blit(self.menu_bg, (0, 0))
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BG_COLOR), self.menu_rect)
        pygame.draw.rect(self.screen, pygame.Color(
            Settings.MENU_BORDER_COLOR), self.menu_rect, 5)
        self.screen.blit(self.title_label, self.title_rect)

        for label, rect in zip(self.text_labels, self.text_rects):
            self.screen.blit(label, rect)

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.back_button)
        self.screen.blit(self.back_label, self.back_rect)

        pygame.display.flip()
        # self.clock.tick(Settings.FPS)
