import pygame
from settings import *


class Dialogue():
    def __init__(self):

        # general setup
        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font2 = pygame.font.Font(UI_FONT, UI_FONT_SIZE+10)

        self.selection_index = 0

        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_RIGHT]:
                self.selection_index = 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
              #  self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time > 300:
                self.can_move = True

    def display(self, name, text):

        self.selection_cooldown()
        self.input()

        # Calculate the height of the dialogue box
        box_height = self.display_surface.get_size()[1] // 5

        # Calculate the vertical position for the dialogue box
        box_y = self.display_surface.get_size()[1] // 1.5

        # Draw the background rectangle for the dialogue box
        pygame.draw.rect(self.display_surface, '#000000',
                         (0, box_y, self.display_surface.get_size()[0], box_height))

        # Render and display the name
        name_surf = self.font.render(name, True, WHITE_TEXT_COLOR)
        name_rect = name_surf.get_rect(
            midtop=(self.display_surface.get_width() // 2, box_y + box_height // 10))
        self.display_surface.blit(name_surf, name_rect)

        # Render and display the text
        text_surf = self.font.render(text, True, WHITE_TEXT_COLOR)
        text_rect = text_surf.get_rect(
            midtop=(self.display_surface.get_width() // 2, box_y + box_height // 4))
        self.display_surface.blit(text_surf, text_rect)

    def display_dialogue_button(self, range_of_player, toggle_dialogue):
        if range_of_player and not toggle_dialogue:
            text_surf = self.font2.render('E', False, BLACK_TEXT_COLOR)
            text_rect = text_surf.get_rect(bottomright=(WIDTH-20, HEIGHT-80))
            pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                             text_rect.inflate(20, 20))
            self.display_surface.blit(text_surf, text_rect)
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
