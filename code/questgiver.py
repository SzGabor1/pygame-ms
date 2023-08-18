from settings import *
import pygame
from npc import NPC
from settings import Settings


class QuestGiver(NPC):
    def __init__(self, npc_name, pos, groups, obstacle_sprites, id):
        super().__init__(npc_name, pos, groups, obstacle_sprites, id)

        self.type = 'questgiver'

        self.id = id

        self.quests = []
        self.load_quests()

        print(self.quests)

        self.toggle_dialogue = False
        self.dialogue = Dialogue(self.accepting_quest,
                                 self.toggle_dialogue)
        self.quest_accepted = False
        self.accept_quest_bool = False

        self.range_of_player = False

    def load_quests(self):
        quest_ids = Settings.npc_data[self.id]['quest_ids']

        for quest_id in quest_ids:
            self.quests.append(quest_id)

    def update_questgiver(self, player):
        self.complete_quest(player)
        self.get_rid_of_completed_quests(player)
        self.display_dialogue(player)
        self.in_range_of_player(player)
        self.display_dialogue_button(player)

        if self.accept_quest_bool:
            self.accept_quest(player)

    def complete_quest(self, player):
        if player.current_amount >= player.max_amount:
            player.is_quest_completed = True
            player.quest_completed_time = pygame.time.get_ticks()
            player.completed_quests.append(player.current_quest)
            player.exp += Settings.quest_data[player.current_quest]['rewardXP']
            player.balance += Settings.quest_data[player.current_quest]['rewardMoney']

            player.quest_accepted = False
            self.accept_quest_bool = False
            player.current_amount = 0

    def get_rid_of_completed_quests(self, player):
        for quest in player.completed_quests:
            if quest in self.quests:
                self.quests.remove(quest)

    def accepting_quest(self, status):
        self.accept_quest_bool = status

    def accept_quest(self, player):
        if not self.quest_accepted and player.current_quest == -1:
            player.current_quest = self.quests[0]
            player.max_amount = Settings.quest_data[self.quests[0]
                                                    ]['max_amount']
            player.quest_accepted = True
            self.accept_quest_bool = False

    def display_dialogue(self, player):
        if self.toggle_dialogue and self.range_of_player and self.quests != [] and player.current_quest == -1 and self.is_questgiver_contains_player_next_quest(player):
            self.dialogue.display(
                self.name, str(Settings.quest_data[self.quests[0]]['text']))

            if self.dialogue.should_close_dialogue():
                self.toggle_dialogue = False

    def display_dialogue_button(self, player):
        if self.quests != [] and player.current_quest == -1 and self.range_of_player and not self.toggle_dialogue and self.is_questgiver_contains_player_next_quest(player):
            self.dialogue.display_dialogue_button()

    def is_questgiver_contains_player_next_quest(self, player):
        if player.completed_quests == [] and 0 in self.quests:
            return True
        elif player.completed_quests != [] and player.completed_quests[-1]+1 in self.quests:
            return True
        else:
            False

    def update(self):
        self.input()

    def npc_update(self, player):
        self.complete_quest(player)
        self.get_rid_of_completed_quests(player)
        self.display_dialogue(player)
        self.in_range_of_player(player)
        self.display_dialogue_button(player)

        if self.accept_quest_bool:
            self.accept_quest(player)


class Dialogue:
    def __init__(self, accepting_quest, toggle_dialogue):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE)
        self.font2 = pygame.font.Font(
            Settings.UI_FONT, Settings.UI_FONT_SIZE + 10)
        self.toggle_dialogue = toggle_dialogue
        self.selection_index = 0
        self.accepting_quest = accepting_quest
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
                if self.selection_index == 1:
                    self.accepting_quest(True)
                self.toggle_dialogue = False
                self.selection_time = pygame.time.get_ticks()

    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                if self.selection_index == 0 and self.left_choice_rect.collidepoint(pos):
                    self.can_move = False
                    self.accepting_quest(False)
                    self.toggle_dialogue = False
                    self.selection_time = pygame.time.get_ticks()
                elif self.selection_index == 1 and self.right_choice_rect.collidepoint(pos):
                    self.can_move = False
                    self.accepting_quest(True)
                    self.toggle_dialogue = False
                    self.selection_time = pygame.time.get_ticks()

    def should_close_dialogue(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_RETURN] and self.selection_index == 0

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time > 300:
                self.can_move = True

    def display_dialogue_button(self):
        text_surf = self.font2.render(
            "E", False, Settings.BLACK_TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(
            Settings.WIDTH - 20, Settings.HEIGHT - 80))
        pygame.draw.rect(self.display_surface, Settings.UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, Settings.UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def display(self, name, text):
        self.selection_cooldown()
        self.input()
        # self.handle_mouse_click()

        box_height = self.display_surface.get_size()[1] // 5
        box_y = self.display_surface.get_size()[1] // 1.5
        dialogue_width = self.display_surface.get_size()[0] / 2
        choice_width = (dialogue_width - 3 * 25) / 2
        left_choice_x = Settings.WIDTH / 4 + 25
        right_choice_x = left_choice_x + choice_width + 25

        self.left_choice_rect = pygame.Rect(
            left_choice_x, box_y + box_height - box_height / 3, choice_width, box_height / 3)

        self.right_choice_rect = pygame.Rect(
            right_choice_x, box_y + box_height - box_height / 3, choice_width, box_height / 3)

        self.draw_dialogue_box()
        self.draw_choice_rectangles(
            self.left_choice_rect, self.right_choice_rect)
        self.draw_choice_text(self.left_choice_rect, self.right_choice_rect)
        self.render_and_display_text(name, text)

    def draw_dialogue_box(self):
        box_height = self.display_surface.get_size()[1] // 5
        box_y = self.display_surface.get_size()[1] // 1.5

        dialogue_rect = (
            Settings.WIDTH / 4, box_y, self.display_surface.get_size()[0] / 2, box_height)

        pygame.draw.rect(self.display_surface,
                         Settings.UI_BG_COLOR, dialogue_rect)
        pygame.draw.rect(self.display_surface,
                         Settings.UI_BORDER_COLOR, dialogue_rect, 3)

    def draw_choice_rectangles(self, left_choice_rect, right_choice_rect):
        if self.selection_index == 0:
            pygame.draw.rect(self.display_surface,
                             Settings.WHITE_TEXT_COLOR, left_choice_rect)
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BORDER_COLOR, left_choice_rect, 3)
        else:
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BG_COLOR, left_choice_rect)
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BORDER_COLOR, left_choice_rect, 3)

        if self.selection_index == 1:
            pygame.draw.rect(self.display_surface,
                             Settings.WHITE_TEXT_COLOR, right_choice_rect)
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BORDER_COLOR, right_choice_rect, 3)
        else:
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BG_COLOR, right_choice_rect)
            pygame.draw.rect(self.display_surface,
                             Settings.UI_BORDER_COLOR, right_choice_rect, 3)

    def draw_choice_text(self, left_choice_rect, right_choice_rect):
        font = pygame.font.Font(None, 30)
        decline_text = font.render(
            "Decline", True, Settings.BLACK_TEXT_COLOR)
        decline_text_rect = decline_text.get_rect(
            center=left_choice_rect.center)
        self.display_surface.blit(decline_text, decline_text_rect)

        accept_text = font.render(
            "Accept", True, Settings.BLACK_TEXT_COLOR)
        accept_text_rect = accept_text.get_rect(
            center=right_choice_rect.center)
        self.display_surface.blit(accept_text, accept_text_rect)

    def render_and_display_text(self, name, text):
        box_height = self.display_surface.get_size()[1] // 5
        box_y = self.display_surface.get_size()[1] // 1.5

        name_surf = self.font.render(
            name, True, Settings.WHITE_TEXT_COLOR)
        name_rect = name_surf.get_rect(
            midtop=(self.display_surface.get_width() // 2, box_y + box_height // 10))
        self.display_surface.blit(name_surf, name_rect)

        text_surf = self.font.render(
            text, True, Settings.WHITE_TEXT_COLOR)
        text_rect = text_surf.get_rect(
            midtop=(self.display_surface.get_width() // 2, box_y + box_height // 4))
        self.display_surface.blit(text_surf, text_rect)
