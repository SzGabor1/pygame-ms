import pygame
import game_api_client
from settings import Settings
import sys
from user import User
from menuenums import menuenums


class UserAuth:
    @staticmethod
    def is_valid_username(username):
        return len(username) >= 5 and username.isalnum()

    @staticmethod
    def is_valid_password(password):
        return len(password) >= 5 and password.isalnum()

    @staticmethod
    def register(username, password):
        username = username
        password = password
        response_info = game_api_client.register_user(username, password)
        print(response_info)

        if response_info['status_code'] == 200:
            print("User registered successfully")
            return True
        else:
            print("User registration failed")
            return False

    @staticmethod
    def login(username, password):
        username = username
        password = password

        try:
            response = game_api_client.login_user(username, password)
            print(response)
            return response
        except ValueError as e:
            print("Login error:", e)
            return False


class LoginPanel():
    def __init__(self, game):
        self.game = game
        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (Settings.WIDTH, Settings.HEIGHT))
        self.username = ""
        self.password = ""
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        self.title_label = self.font.render(
            "Login", True, Settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 200))

        self.menu_width = 500
        self.menu_height = 500
        self.menu_x = (Settings.WIDTH - self.menu_width) // 2
        self.menu_y = (Settings.HEIGHT - self.menu_height) // 2 - 100

        self.menu_rect = pygame.Rect(
            self.menu_x, self.menu_y + 100, self.menu_width, self.menu_height)

        self.username_label = self.font.render(
            "Username:", True, Settings.BLACK_TEXT_COLOR)
        self.name_rect = self.username_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 150))

        self.password_label = self.font.render(
            "Password:", True, Settings.BLACK_TEXT_COLOR)
        self.password_rect = self.password_label.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 - 80))

        self.password_input_rect = pygame.Rect(
            Settings.WIDTH // 2 - 100, Settings.HEIGHT // 2 - 60, 200, 30)
        self.password_masked = True  # Flag to toggle password masking

        self.name_input_rect = pygame.Rect(
            Settings.WIDTH // 2 - 100, Settings.HEIGHT // 2 - 130, 200, 30)

        self.login_button = pygame.Rect(
            Settings.WIDTH // 2 - 100, Settings.HEIGHT // 2 + 150, 80, 30)
        self.login_label = self.font.render(
            "Login", True, Settings.BLACK_TEXT_COLOR)
        self.login_rect = self.login_label.get_rect(
            center=self.login_button.center)

        self.register_button = pygame.Rect(
            Settings.WIDTH // 2 + 20, Settings.HEIGHT // 2 + 150, 120, 30)
        self.register_label = self.font.render(
            "Register", True, Settings.BLACK_TEXT_COLOR)
        self.register_rect = self.register_label.get_rect(
            center=self.register_button.center)

        self.offline_button = pygame.Rect(
            Settings.WIDTH // 2 - 100, Settings.HEIGHT // 2 + 70, 200, 30)
        self.offline_label = self.font.render(
            "Offline Mode", True, Settings.BLACK_TEXT_COLOR)
        self.offline_rect = self.offline_label.get_rect(
            center=self.offline_button.center)

        self.active_input = None

        self.success_message = self.font.render(
            "Successful registration!", True, Settings.GREEN_TEXT_COLOR)
        self.success_message_rect = self.success_message.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 200))

        self.failure_message = self.font.render(
            "Registration failed.", True, Settings.RED_TEXT_COLOR)
        self.failure_message_rect = self.failure_message.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 200))

        self.login_failure_message = self.font.render(
            "Login failed: Invalid credentials", True, Settings.RED_TEXT_COLOR)
        self.login_failure_message_rect = self.login_failure_message.get_rect(
            center=(Settings.WIDTH // 2, Settings.HEIGHT // 2 + 200))

        self.show_success_message = False
        self.show_failure_message = False
        self.show_login_failure_message = False

    def render(self):
        self.screen.blit(self.menu_bg, (0, 0))
        pygame.draw.rect(self.screen, Settings.MENU_BG_COLOR, self.menu_rect)
        pygame.draw.rect(
            self.screen, Settings.BLACK_TEXT_COLOR, self.menu_rect, 2)

        self.screen.blit(self.title_label, self.title_rect)
        self.screen.blit(self.username_label, self.name_rect)
        pygame.draw.rect(self.screen, Settings.BLACK_TEXT_COLOR,
                         self.name_input_rect, 2)

        username_input = self.font.render(
            self.username, True, Settings.BLACK_TEXT_COLOR)
        self.screen.blit(
            username_input, (self.name_input_rect.x + 5, self.name_input_rect.y + 5))

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.login_button)
        self.screen.blit(self.login_label, self.login_rect)

        self.screen.blit(self.password_label, self.password_rect)
        pygame.draw.rect(self.screen, Settings.BLACK_TEXT_COLOR,
                         self.password_input_rect, 2)

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.register_button)
        self.screen.blit(self.register_label, self.register_rect)

        pygame.draw.rect(
            self.screen, Settings.MENU_BUTTON_BG_COLOR, self.offline_button)
        self.screen.blit(self.offline_label, self.offline_rect)

        if self.password_masked:
            masked_password = '*' * len(self.password)
            password_input = self.font.render(
                masked_password, True, Settings.BLACK_TEXT_COLOR)
        else:
            password_input = self.font.render(
                self.password, True, Settings.BLACK_TEXT_COLOR)

        self.screen.blit(
            password_input, (self.password_input_rect.x + 5, self.password_input_rect.y + 5))

        if self.show_success_message:
            self.screen.blit(self.success_message, self.success_message_rect)

        if self.show_failure_message:
            self.screen.blit(self.failure_message, self.failure_message_rect)

        if self.show_login_failure_message:
            self.screen.blit(self.login_failure_message,
                             self.login_failure_message_rect)

        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.handle_input(event)

        self.render()
        pygame.display.flip()

    def handle_input(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.name_input_rect.collidepoint(mouse_pos):
                self.active_input = "username"  # Activate username input field
                self.username = ""
            elif self.password_input_rect.collidepoint(mouse_pos):
                self.active_input = "password"  # Activate password input field
                self.password = ""
            else:
                self.active_input = None  # Deactivate any active input field

            if self.login_button.collidepoint(mouse_pos):
                # Handle login button click
                response = UserAuth.login(self.username, self.password)
                if response and response != 401:
                    self.game.user = User(
                        response['username'], response['user_id'])
                    self.game.online = True
                    self.game.state = menuenums.MENU
                else:
                    # Display login failure message
                    self.show_login_failure_message = True
                    self.show_success_message = False
                    self.show_failure_message = False

            if self.offline_button.collidepoint(mouse_pos):
                self.game.state = menuenums.MENU
                pass

            if self.register_button.collidepoint(mouse_pos):
                if UserAuth.is_valid_username(self.username) and UserAuth.is_valid_password(self.password):
                    response = UserAuth.register(self.username, self.password)
                    if response:
                        self.show_success_message = True
                        self.show_login_failure_message = False
                        self.show_failure_message = False
                    else:
                        self.show_failure_message = True
                        self.show_login_failure_message = False
                        self.show_success_message = False
                else:
                    self.show_failure_message = True

        if event.type == pygame.KEYDOWN and self.active_input:
            if self.active_input == "username":
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
            elif self.active_input == "password":
                if event.key == pygame.K_BACKSPACE:
                    self.password = self.password[:-1]
                else:
                    self.password += event.unicode
