import pygame
from settings import *


class Dialogue:
    def __init__(self, accept_quest, toggle_dialogue):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.font2 = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 10)
        self.toggle_dialogue = toggle_dialogue
        self.selection_index = 0
        self.accept_quest = accept_quest
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

            if keys[pygame.K_RETURN]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                if self.selection_index == 1:
                    self.accept_quest()
                self.toggle_dialogue = False

    def should_close_dialogue(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_RETURN] and self.selection_index == 0

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time > 300:
                self.can_move = True

    def display_dialogue_button(self):
        text_surf = self.font2.render("E", False, BLACK_TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(WIDTH - 20, HEIGHT - 80))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def display(self, name, text):
        self.selection_cooldown()
        self.input()

        box_height = self.display_surface.get_size()[1] // 5
        box_y = self.display_surface.get_size()[1] // 1.5
        dialogue_width = self.display_surface.get_size()[0] / 2
        choice_width = (dialogue_width - 3 * 25) / 2
        left_choice_x = WIDTH / 4 + 25
        right_choice_x = left_choice_x + choice_width + 25

        left_choice_rect = pygame.Rect(
            left_choice_x, box_y + box_height - box_height / 3, choice_width, box_height / 3)

        right_choice_rect = pygame.Rect(
            right_choice_x, box_y + box_height - box_height / 3, choice_width, box_height / 3)

        self.draw_dialogue_box()
        self.draw_choice_rectangles(left_choice_rect, right_choice_rect)
        self.draw_choice_text(left_choice_rect, right_choice_rect)
        self.render_and_display_text(name, text)

    def draw_dialogue_box(self):
        box_height = self.display_surface.get_size()[1] // 5
        box_y = self.display_surface.get_size()[1] // 1.5

        dialogue_rect = (
            WIDTH / 4, box_y, self.display_surface.get_size()[0] / 2, box_height)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, dialogue_rect)
        pygame.draw.rect(self.display_surface,
                         UI_BORDER_COLOR, dialogue_rect, 3)

    def draw_choice_rectangles(self, left_choice_rect, right_choice_rect):
        if self.selection_index == 0:
            pygame.draw.rect(self.display_surface,
                             WHITE_TEXT_COLOR, left_choice_rect)
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR, left_choice_rect, 3)
        else:
            pygame.draw.rect(self.display_surface,
                             UI_BG_COLOR, left_choice_rect)
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR, left_choice_rect, 3)

        if self.selection_index == 1:
            pygame.draw.rect(self.display_surface,
                             WHITE_TEXT_COLOR, right_choice_rect)
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR, right_choice_rect, 3)
        else:
            pygame.draw.rect(self.display_surface,
                             UI_BG_COLOR, right_choice_rect)
            pygame.draw.rect(self.display_surface,
                             UI_BORDER_COLOR, right_choice_rect, 3)

    def draw_choice_text(self, left_choice_rect, right_choice_rect):
        font = pygame.font.Font(None, 30)
        decline_text = font.render("Decline", True, BLACK_TEXT_COLOR)
        decline_text_rect = decline_text.get_rect(
            center=left_choice_rect.center)
        self.display_surface.blit(decline_text, decline_text_rect)

        accept_text = font.render("Accept", True, BLACK_TEXT_COLOR)
        accept_text_rect = accept_text.get_rect(
            center=right_choice_rect.center)
        self.display_surface.blit(accept_text, accept_text_rect)

    def render_and_display_text(self, name, text):
        box_height = self.display_surface.get_size()[1] // 5
        box_y = self.display_surface.get_size()[1] // 1.5

        name_surf = self.font.render(name, True, WHITE_TEXT_COLOR)
        name_rect = name_surf.get_rect(
            midtop=(self.display_surface.get_width() // 2, box_y + box_height // 10))
        self.display_surface.blit(name_surf, name_rect)

        text_surf = self.font.render(text, True, WHITE_TEXT_COLOR)
        text_rect = text_surf.get_rect(
            midtop=(self.display_surface.get_width() // 2, box_y + box_height // 4))
        self.display_surface.blit(text_surf, text_rect)
