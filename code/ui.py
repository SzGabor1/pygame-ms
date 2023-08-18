import pygame
from settings import *


class UI:
    def __init__(self, ):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, Settings.HEALTH_BAR_WIDTH, Settings.BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 37, Settings.ENERGY_BAR_WIDTH, Settings.BAR_HEIGHT)

        # weapon dictionary
        self.weapon_graphics = []
        for weapon in Settings.weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # item dictionary
        self.potion_graphics = []
        for potion in Settings.items.values():
            path = potion['graphic']
            potion_image = pygame.image.load(path).convert_alpha()
            self.potion_graphics.append(potion_image)

    def show_bar(self, current, max, bg_rect, color):
        pygame.draw.rect(self.display_surface,
                         Settings.UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, color, (bg_rect.x,
                         bg_rect.y, bg_rect.width * (current/max), bg_rect.height))
        pygame.draw.rect(self.display_surface,
                         Settings.UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(
            str(int(exp)), False, Settings.BLACK_TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(
            Settings.WIDTH-10, Settings.HEIGHT-10))
        pygame.draw.rect(self.display_surface, Settings.UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, Settings.UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def show_objective(self, objective):
        text_surf = self.font.render(
            (objective), False, Settings.WHITE_TEXT_COLOR)
        text_rect = text_surf.get_rect(
            topright=(Settings.WIDTH-10, 200))
        pygame.draw.rect(self.display_surface, Settings.UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, Settings.UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def show_weapon(self, left, top, weapon_index):
        bg_rect = pygame.Rect(
            left, top, Settings.ITEM_BOX_SIZE, Settings.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,
                         Settings.UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface,
                         Settings.UI_BORDER_COLOR, bg_rect, 3)

        weapon_image = pygame.transform.scale(
            self.weapon_graphics[weapon_index], (Settings.ITEM_BOX_SIZE, Settings.ITEM_BOX_SIZE))
        self.display_surface.blit(weapon_image, (left, top))

    def show_inventory(self, player):

        # Player inventory
        player_inventory = player.inventory.items
        inventory_size = 5  # Fix inventory size to 5 slots
        start_x = (Settings.WIDTH - (inventory_size *
                                     Settings.ITEM_BOX_SIZE)) // 2
        inventory_y = Settings.HEIGHT - Settings.ITEM_BOX_SIZE - 10

        for i in range(inventory_size):
            if i < len(player_inventory):
                item_id = player_inventory[i]
                if item_id in Settings.items:
                    item = Settings.items[item_id]
                    path = item['graphic']
                    item_image = pygame.image.load(path).convert_alpha()
                    item_image = pygame.transform.scale(
                        item_image, (Settings.ITEM_BOX_SIZE - 6, Settings.ITEM_BOX_SIZE - 6))
            else:
                # Use a default image for empty slots
                item_image = pygame.Surface(
                    (Settings.ITEM_BOX_SIZE - 6, Settings.ITEM_BOX_SIZE - 6))
                item_image.fill(Settings.MENU_BG_COLOR)

            item_rect = pygame.Rect(start_x + (i * Settings.ITEM_BOX_SIZE), inventory_y,
                                    Settings.ITEM_BOX_SIZE, Settings.ITEM_BOX_SIZE)

            # Determine if the item is selected
            selected = (i == player.inventory_index)

            # Draw slot background
            if selected:
                pygame.draw.rect(self.display_surface,
                                 Settings.INVENTORY_SELECTED_BG_COLOR, item_rect)
            else:
                pygame.draw.rect(self.display_surface,
                                 Settings.MENU_BG_COLOR, item_rect)

            # Draw item image inside the slot
            item_image_rect = item_image.get_rect(center=item_rect.center)
            self.display_surface.blit(item_image, item_image_rect.topleft)

            # Draw slot border
            pygame.draw.rect(self.display_surface,
                             Settings.MENU_BORDER_COLOR, item_rect, 3)

    def show_completed_quest(self, player):
        if player.is_quest_completed:
            objective = Settings.quest_data[player.current_quest]['objective']
            rewardXP = Settings.quest_data[player.current_quest]['rewardXP']
            rewardMoney = Settings.quest_data[player.current_quest]['rewardMoney']
            quest_completed_msg = "Quest Completed!"

            # Render the text surfaces
            objective_surf = self.font.render(
                objective, False, Settings.WHITE_TEXT_COLOR)
            rewardXP_surf = self.font.render(
                str(rewardXP) + " xp", False, Settings.WHITE_TEXT_COLOR)
            rewardMoney_surf = self.font.render(
                str(rewardMoney) + " gold", False, Settings.WHITE_TEXT_COLOR)
            quest_completed_surf = self.font.render(
                quest_completed_msg, False, Settings.WHITE_TEXT_COLOR)

            # Calculate the rectangle dimensions and positions
            text_width = max(objective_surf.get_width(), rewardXP_surf.get_width(
            ), rewardMoney_surf.get_width(), quest_completed_surf.get_width())
            text_height = objective_surf.get_height() + rewardXP_surf.get_height() + \
                rewardMoney_surf.get_height() + quest_completed_surf.get_height() + 40
            text_rect = pygame.Rect(
                (Settings.WIDTH - text_width) // 2, 10, text_width, text_height)

            # Draw the background rectangle
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BG_COLOR, text_rect)
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BORDER_COLOR, text_rect, 3)

            # Position and blit the text surfaces
            quest_completed_rect = quest_completed_surf.get_rect(
                center=(Settings.WIDTH // 2, text_rect.y + 20))
            objective_rect = objective_surf.get_rect(
                center=(Settings.WIDTH // 2, quest_completed_rect.bottom + 30))
            rewardXP_rect = rewardXP_surf.get_rect(
                center=(Settings.WIDTH // 2, objective_rect.bottom + 10))
            rewardMoney_rect = rewardMoney_surf.get_rect(
                center=(Settings.WIDTH // 2, rewardXP_rect.bottom + 10))

            self.display_surface.blit(
                quest_completed_surf, quest_completed_rect)
            self.display_surface.blit(objective_surf, objective_rect)
            self.display_surface.blit(rewardXP_surf, rewardXP_rect)
            self.display_surface.blit(rewardMoney_surf, rewardMoney_rect)

    def caculate_strength_potion_time(self, player):
        current_time = pygame.time.get_ticks()
        return int((player.strength_potion_duration)/1000)-(int((current_time - player.strength_potion_time) / 1000))

    def show_strength_potion_duration(self, player):
        if player.used_strength_potion:

            # Draw background and border
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BG_COLOR, (100, 100, 40, 40))
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BORDER_COLOR, (100, 100, 40, 40), 2)

            # Load the strength potion image here
            strength_potion_image = pygame.image.load(
                "graphics/items/strength_potion.png")

            strength_potion_image = pygame.transform.scale(
                strength_potion_image, (40, 40))

            # Calculate the blit position to center the image inside the rectangle
            image_x = 100 + (40 - strength_potion_image.get_width()) // 2
            image_y = 100 + (40 - strength_potion_image.get_height()) // 2

            self.display_surface.blit(
                strength_potion_image, (image_x, image_y))

            # Display the potion duration on top of the image
            text_surf = self.font.render(
                f"{self.caculate_strength_potion_time(player)}", True, Settings.WHITE_TEXT_COLOR)
            text_rect = text_surf.get_rect(
                center=(100 + 40 // 2, 100 + 40 // 2))
            self.display_surface.blit(text_surf, text_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, Settings.HEALTH_COLOR)
        self.show_bar(
            player.energy, player.stats['energy'], self.energy_bar_rect, Settings.ENERGY_COLOR)
        self.show_exp(player.exp)
        self.show_weapon(10, Settings.HEIGHT - 10 -
                         Settings.ITEM_BOX_SIZE, player.weapon_index)

        if player.current_quest != -1 and not player.is_quest_completed:
            self.show_objective(Settings.quest_data[player.current_quest]['objective'] +
                                " " +
                                str(Settings.quest_data[player.current_quest]['max_amount']
                                    ) + "/" + str(player.current_amount))
        self.show_inventory(player)
        self.show_strength_potion_duration(player)

        # should create alert class to handle these
        self.show_completed_quest(player)
        self.show_game_over(player)

    def show_game_over(self, player):
        if player.game_over:
            self.show_save_warning()
            game_over_msg = "Game Over!"

            # Render the text surface
            game_over_surf = self.font.render(
                game_over_msg, False, Settings.WHITE_TEXT_COLOR)

            # Calculate the rectangle dimensions and positions
            text_width = game_over_surf.get_width()
            text_height = game_over_surf.get_height() + 40
            text_rect = pygame.Rect(
                (Settings.WIDTH - text_width) // 2, 10, text_width, text_height)

            # Draw the background rectangle
            pygame.draw.rect(self.display_surface,
                             Settings.MENU_BG_COLOR, text_rect)
            pygame.draw.rect(self.display_surface,
                             Settings.MENU_BORDER_COLOR, text_rect, 3)

            # Position and blit the text surface
            game_over_rect = game_over_surf.get_rect(
                center=(Settings.WIDTH // 2, text_rect.y + 20))

            self.display_surface.blit(
                game_over_surf, game_over_rect)

    def show_save_warning(self):
        save_warning_msg = "SAVE GAME BEFORE EXIT"

        # Render the red text surface
        save_warning_surf = self.font.render(
            save_warning_msg, False, (255, 0, 0))  # Red color

        # Calculate the rectangle dimensions and positions
        text_width = save_warning_surf.get_width()
        text_height = save_warning_surf.get_height() + 40
        text_rect = pygame.Rect(
            (Settings.WIDTH - text_width) // 2, 120, text_width, text_height)

        # Draw the background rectangle (in a different color, e.g., black)
        pygame.draw.rect(self.display_surface,
                         Settings.MENU_BG_COLOR, text_rect)  # Black background
        pygame.draw.rect(self.display_surface,
                         Settings.MENU_BORDER_COLOR, text_rect, 3)

        # Position and blit the text surface
        save_warning_rect = save_warning_surf.get_rect(
            center=(Settings.WIDTH // 2, text_rect.y + 20))

        self.display_surface.blit(
            save_warning_surf, save_warning_rect)
