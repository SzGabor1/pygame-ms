import pygame
from settings import *


class UI:
    def __init__(self, settings):

        # general
        self.settings = settings
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(
            self.settings.UI_FONT, self.settings.UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, self.settings.HEALTH_BAR_WIDTH, self.settings.BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 37, self.settings.ENERGY_BAR_WIDTH, self.settings.BAR_HEIGHT)

        # weapon dictionary
        self.weapon_graphics = []
        for weapon in self.settings.weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # item dictionary
        self.potion_graphics = []
        for potion in self.settings.items.values():
            path = potion['graphic']
            potion_image = pygame.image.load(path).convert_alpha()
            self.potion_graphics.append(potion_image)

    def show_bar(self, current, max, bg_rect, color):
        pygame.draw.rect(self.display_surface,
                         self.settings.UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, color, (bg_rect.x,
                         bg_rect.y, bg_rect.width * (current/max), bg_rect.height))
        pygame.draw.rect(self.display_surface,
                         self.settings.UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(
            str(int(exp)), False, self.settings.BLACK_TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(
            self.settings.WIDTH-10, self.settings.HEIGHT-10))
        pygame.draw.rect(self.display_surface, self.settings.UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, self.settings.UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def show_objective(self, objective):
        text_surf = self.font.render(
            (objective), False, self.settings.WHITE_TEXT_COLOR)
        text_rect = text_surf.get_rect(
            topright=(self.settings.WIDTH-10, 200))  # Módosított sor
        pygame.draw.rect(self.display_surface, self.settings.UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, self.settings.UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def show_weapon(self, left, top, weapon_index):
        bg_rect = pygame.Rect(
            left, top, self.settings.ITEM_BOX_SIZE, self.settings.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,
                         self.settings.UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface,
                         self.settings.UI_BORDER_COLOR, bg_rect, 3)

        weapon_image = pygame.transform.scale(
            self.weapon_graphics[weapon_index], (self.settings.ITEM_BOX_SIZE, self.settings.ITEM_BOX_SIZE))
        self.display_surface.blit(weapon_image, (left, top))

    def show_inventory(self, player):

        # Player inventory
        player_inventory = player.inventory.items
        inventory_size = 5  # Fix inventory size to 5 slots
        start_x = (self.settings.WIDTH - (inventory_size *
                                          self.settings.ITEM_BOX_SIZE)) // 2
        inventory_y = self.settings.HEIGHT - self.settings.ITEM_BOX_SIZE - 10

        for i in range(inventory_size):
            if i < len(player_inventory):
                item_id = player_inventory[i]
                if item_id in self.settings.items:
                    item = self.settings.items[item_id]
                    path = item['graphic']
                    item_image = pygame.image.load(path).convert_alpha()
                    item_image = pygame.transform.scale(
                        item_image, (self.settings.ITEM_BOX_SIZE - 6, self.settings.ITEM_BOX_SIZE - 6))
            else:
                # Use a default image for empty slots
                item_image = pygame.Surface(
                    (self.settings.ITEM_BOX_SIZE - 6, self.settings.ITEM_BOX_SIZE - 6))
                item_image.fill(self.settings.MENU_BG_COLOR)

            item_rect = pygame.Rect(start_x + (i * self.settings.ITEM_BOX_SIZE), inventory_y,
                                    self.settings.ITEM_BOX_SIZE, self.settings.ITEM_BOX_SIZE)

            # Determine if the item is selected
            selected = (i == player.inventory_index)

            # Draw slot background
            if selected:
                pygame.draw.rect(self.display_surface,
                                 self.settings.INVENTORY_SELECTED_BG_COLOR, item_rect)
            else:
                pygame.draw.rect(self.display_surface,
                                 self.settings.MENU_BG_COLOR, item_rect)

            # Draw item image inside the slot
            item_image_rect = item_image.get_rect(center=item_rect.center)
            self.display_surface.blit(item_image, item_image_rect.topleft)

            # Draw slot border
            pygame.draw.rect(self.display_surface,
                             self.settings.MENU_BORDER_COLOR, item_rect, 3)

    def show_completed_quest(self, player):
        if player.is_quest_completed:
            objective = self.settings.quest_data[player.current_quest]['objective']
            rewardXP = self.settings.quest_data[player.current_quest]['rewardXP']
            rewardMoney = self.settings.quest_data[player.current_quest]['rewardMoney']
            quest_completed_msg = "Quest Completed!"

            # Render the text surfaces
            objective_surf = self.font.render(
                objective, False, self.settings.WHITE_TEXT_COLOR)
            rewardXP_surf = self.font.render(
                str(rewardXP) + " xp", False, self.settings.WHITE_TEXT_COLOR)
            rewardMoney_surf = self.font.render(
                str(rewardMoney) + " gold", False, self.settings.WHITE_TEXT_COLOR)
            quest_completed_surf = self.font.render(
                quest_completed_msg, False, self.settings.WHITE_TEXT_COLOR)

            # Calculate the rectangle dimensions and positions
            text_width = max(objective_surf.get_width(), rewardXP_surf.get_width(
            ), rewardMoney_surf.get_width(), quest_completed_surf.get_width())
            text_height = objective_surf.get_height() + rewardXP_surf.get_height() + \
                rewardMoney_surf.get_height() + quest_completed_surf.get_height() + 40
            text_rect = pygame.Rect(
                (self.settings.WIDTH - text_width) // 2, 10, text_width, text_height)

            # Draw the background rectangle
            pygame.draw.rect(self.display_surface,
                             self.settings.UI_BG_COLOR, text_rect)
            pygame.draw.rect(self.display_surface,
                             self.settings.UI_BORDER_COLOR, text_rect, 3)

            # Position and blit the text surfaces
            quest_completed_rect = quest_completed_surf.get_rect(
                center=(self.settings.WIDTH // 2, text_rect.y + 20))
            objective_rect = objective_surf.get_rect(
                center=(self.settings.WIDTH // 2, quest_completed_rect.bottom + 30))
            rewardXP_rect = rewardXP_surf.get_rect(
                center=(self.settings.WIDTH // 2, objective_rect.bottom + 10))
            rewardMoney_rect = rewardMoney_surf.get_rect(
                center=(self.settings.WIDTH // 2, rewardXP_rect.bottom + 10))

            self.display_surface.blit(
                quest_completed_surf, quest_completed_rect)
            self.display_surface.blit(objective_surf, objective_rect)
            self.display_surface.blit(rewardXP_surf, rewardXP_rect)
            self.display_surface.blit(rewardMoney_surf, rewardMoney_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, self.settings.HEALTH_COLOR)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, self.settings.ENERGY_COLOR)
        self.show_exp(player.exp)
        self.show_weapon(10, self.settings.HEIGHT - 10 -
                         self.settings.ITEM_BOX_SIZE, player.weapon_index)

        if player.current_quest != -1 and not player.is_quest_completed:
            self.show_objective(self.settings.quest_data[player.current_quest]['objective'] +
                                " " +
                                str(self.settings.quest_data[player.current_quest]['max_amount']
                                    ) + "/" + str(player.current_amount))
        self.show_inventory(player)
        self.show_completed_quest(player)
