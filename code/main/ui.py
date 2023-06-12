import pygame
from settings import *


class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(
            10, 37, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self, current, max, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, color, (bg_rect.x,
                         bg_rect.y, bg_rect.width * (current/max), bg_rect.height))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(WIDTH-10, HEIGHT-10))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def show_weapon(self, left, top, weapon_index):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        weapon_image = pygame.transform.scale(
            self.weapon_graphics[weapon_index], (ITEM_BOX_SIZE, ITEM_BOX_SIZE))
        self.display_surface.blit(weapon_image, (left, top))

    def display(self, palyer):
        self.show_bar(
            palyer.health, palyer.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(
            palyer.energy, palyer.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(palyer.exp)
        self.show_weapon(10, HEIGHT - 10 - ITEM_BOX_SIZE, palyer.weapon_index)
