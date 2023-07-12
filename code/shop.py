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
            center=(self.settings.WIDTH // 2, self.settings.HEIGHT // 2 - 200))

        # Define the rectangle for the menu background
        menu_width = 400
        menu_height = 600
        menu_x = (self.settings.WIDTH - menu_width) // 2
        # Adjust the value here
        menu_y = (self.settings.HEIGHT - menu_height) // 2

        self.menu_rect = pygame.Rect(
            menu_x, menu_y+50, menu_width, menu_height)

        self.close_button = pygame.Rect(
            menu_x + 50, menu_y + 550, 300, 50)
        self.close_label = self.font.render(
            "Close", True, self.settings.BLACK_TEXT_COLOR)
        self.close_rect = self.close_label.get_rect(
            center=self.close_button.center)

    def display(self, player, events):
        pygame.draw.rect(self.display_surface, pygame.Color(
            self.settings.MENU_BG_COLOR), self.menu_rect)

        pygame.draw.rect(self.display_surface, pygame.Color(
            self.settings.MENU_BORDER_COLOR), self.menu_rect, 5)

        self.display_surface.blit(self.title_label, self.title_rect)
        pygame.draw.rect(self.display_surface, self.settings.MENU_BUTTON_BG_COLOR,
                         self.close_button)
        self.display_surface.blit(self.close_label, self.close_rect)

        # Display items for sale
        item_size = 80
        item_padding = 20
        item_start_x = self.menu_rect.left + 20
        item_start_y = self.menu_rect.top + 100

        for index, item_id in enumerate(self.itemlist):
            item = self.settings.items[item_id]

            item_rect = pygame.Rect(
                item_start_x + (item_size + item_padding) * (index % 3),
                item_start_y + (item_size + item_padding) * (index // 3),
                item_size, item_size
            )

            item_image = pygame.image.load(item['graphic']).convert_alpha()
            item_image = pygame.transform.scale(
                item_image, (item_size, item_size))

            self.display_surface.blit(item_image, item_rect.topleft)

            # Display item cost
            item_cost = item['cost']
            item_cost_label = self.font.render(
                f"{item_cost}", True, self.settings.BLACK_TEXT_COLOR)
            item_cost_rect = item_cost_label.get_rect(
                bottomleft=(item_rect.left, item_rect.bottom + 15))
            self.display_surface.blit(item_cost_label, item_cost_rect)

            # Check if the mouse is hovering over the item
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                item_name = item['name']
                item_description = item['description']
                item_info = f"{item_name}: {item_description}"

                item_info_label = self.font.render(
                    item_info, True, self.settings.BLACK_TEXT_COLOR)
                item_info_rect = item_info_label.get_rect(
                    bottomleft=(self.menu_rect.left + 20, self.menu_rect.bottom - 20))
                self.display_surface.blit(item_info_label, item_info_rect)

            # Check if the item is double-clicked
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and item_rect.collidepoint(event.pos):
                    if player.balance >= item_cost:
                        player.inventory.add_item(item_id)
                        player.balance -= item_cost
                        print(f"Purchased {item['name']}")
                    else:
                        print("Insufficient funds!")

        # Display player's balance
        balance_label = self.font.render(
            f"Balance: {player.balance}", True, self.settings.BLACK_TEXT_COLOR)
        balance_rect = balance_label.get_rect(
            bottomleft=(self.menu_rect.left + 20, self.menu_rect.bottom - 170))
        self.display_surface.blit(balance_label, balance_rect)

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
