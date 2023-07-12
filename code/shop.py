import pygame
import sys


class Shop():
    def __init__(self, settings, item_list, toggle_shop, npc_name):
        self.settings = settings
        self.itemlist = item_list
        self.npc_name = npc_name

        self.toggle_shop = toggle_shop

        self.init_shop()

    def init_shop(self):
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            self.settings.UI_FONT, self.settings.UI_FONT_SIZE)

        self.title_label = self.font.render(
            self.npc_name, True, self.settings.BLACK_TEXT_COLOR)
        self.title_rect = self.title_label.get_rect(
            center=(self.settings.WIDTH // 2, self.settings.HEIGHT // 2 - 100))

        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 400
        menu_x = (self.settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (self.settings.HEIGHT - menu_height) // 2

        self.menu_rect = pygame.Rect(
            menu_x, menu_y+50, menu_width, menu_height)

        self.close_button = pygame.Rect(
            menu_x + 50, menu_y + 350, 300, 50)
        self.close_label = self.font.render(
            "Close", True, self.settings.BLACK_TEXT_COLOR)
        self.close_rect = self.close_label.get_rect(
            center=self.close_button.center)

    def display(self, player):
        pygame.draw.rect(self.display_surface, pygame.Color(
            self.settings.MENU_BG_COLOR), self.menu_rect)

        pygame.draw.rect(self.display_surface, pygame.Color(
            self.settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.display_surface.blit(self.title_label, self.title_rect)
        pygame.draw.rect(self.display_surface, self.settings.MENU_BUTTON_BG_COLOR,
                         self.close_button)
        self.display_surface.blit(self.close_label, self.close_rect)

    def display_shop_button(self):
        text_surf = self.font.render(
            "E", False, self.settings.BLACK_TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(
            self.settings.WIDTH - 20, self.settings.HEIGHT - 80))
        pygame.draw.rect(self.display_surface, self.settings.UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, self.settings.UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.close_button.collidepoint(event.pos):
                        print("Close button clicked!")
                        self.toggle_shop()
