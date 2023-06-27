import sys
import pygame
from mainmenu import SettingsMenu


class IngameMenu:
    def __init__(self, settings, toggle_menu):
        self.display_surface = pygame.display.get_surface()
        self.toggle_menu = toggle_menu
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(
            settings.UI_FONT, settings.UI_FONT_SIZE)

        self.menu_bg = pygame.transform.scale(pygame.image.load(
            "graphics/Backgrounds/menubg.jpg"), (settings.WIDTH, settings.HEIGHT))

        self.menu_items = ["Resume", "Save", "Settings", "Exit"]
        self.menu_item_height = self.font.get_height() + 10
        self.menu_width = 400
        self.menu_height = len(self.menu_items) * self.menu_item_height + 20
        self.menu_x = (settings.WIDTH - self.menu_width) // 2
        self.menu_y = (settings.HEIGHT - self.menu_height) // 2 + 50
        self.menu_rect = pygame.Rect(
            self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        self.menu_items_rects = []
        self.selected_item = 0

        self.settings = settings
        self.cooldown_time = 500  # milliseconds
        self.last_click_time = 0

    def display(self):
        self.update()
        self.render()

    def update(self):
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
                        self.toggle_menu("")
                        # Resume the game
                    elif selected_item == "Save":
                        print("Save button clicked!")
                        # Save the game
                    elif selected_item == "Settings":
                        print("Settings button clicked!")
                        # Open settings menu
                        settings_menu = SettingsMenu()
                        settings_menu.run()
                    elif selected_item == "Exit":
                        print("Exit button clicked!")
                        pygame.quit()
                        sys.exit()

    def render(self):
        self.display_surface.blit(self.menu_bg, (0, 0))

        pygame.draw.rect(self.display_surface, pygame.Color(
            self.settings.MENU_BG_COLOR), self.menu_rect)
        pygame.draw.rect(self.display_surface, pygame.Color(
            self.settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.menu_items_rects = []  # Clear the previous menu item rectangles

        for index, item in enumerate(self.menu_items):
            item_surf = self.font.render(
                item, True, self.settings.BLACK_TEXT_COLOR)
            item_rect = item_surf.get_rect(center=(
                self.menu_rect.centerx, self.menu_rect.top + self.menu_item_height * index + self.menu_item_height // 2))
            self.menu_items_rects.append(item_rect)
            self.display_surface.blit(item_surf, item_rect)

        pygame.display.flip()
        self.clock.tick(self.settings.FPS)
