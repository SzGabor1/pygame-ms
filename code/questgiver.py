import pygame
from npc import NPC
from settings import Settings
from dialogue import Dialogue


class QuestGiver(NPC):
    def __init__(self, npc_name, pos, groups, obstacle_sprites, quests, id):
        super().__init__(npc_name, pos, groups, obstacle_sprites, id)

        self.quests = quests

        self.toggle_dialogue = False
        self.dialogue = Dialogue(self.accepting_quest,
                                 self.toggle_dialogue)
        self.quest_accepted = False
        self.accept_quest_bool = False

        self.range_of_player = False

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
        if self.toggle_dialogue and self.range_of_player and self.quests != [] and player.current_quest == -1:
            self.dialogue.display(
                self.name, str(Settings.quest_data[self.quests[0]]['text']))

            if self.dialogue.should_close_dialogue():
                self.toggle_dialogue = False

    def display_dialogue_button(self, player):
        if self.quests != [] and player.current_quest == -1 and self.range_of_player and not self.toggle_dialogue:
            self.dialogue.display_dialogue_button()

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
