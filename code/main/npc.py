from typing import Any
import pygame
from entity import Entity
from support import *
from settings import *
from dialogue import Dialogue


class NPC(Entity):
    def __init__(self, npc_name, pos, groups, obstacle_sprites, quests, player):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'npc'

        # graphics setup
        self.import_graphics(npc_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites

        self.player = player

        # stats
        self.npc_name = npc_name
        self.npc_pos = pos
        self.quests = quests

        # self.player interaction
        self.range_of_player = False
        self.toggle_dialogue = False
        self.dialogue = Dialogue(self.accept_quest, self.toggle_dialogue)
        self.quest_accepted = False

        self.display_surface = pygame.display.get_surface()

    def import_graphics(self, name):
        self.animations = {'idle': []}
        main_path = f'graphics/Characters/Villager1/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.toggle_dialogue = True

    def in_range_of_player(self):
        player_pos = self.player.rect.center
        distance = pygame.math.Vector2(self.npc_pos) - player_pos
        if distance.length() <= 100:
            self.range_of_player = True
        else:
            self.range_of_player = False
            self.toggle_dialogue = False

    def update(self):

        self.input()
        self.show_dialogue_button()
        self.in_range_of_player()
        self.show_dialogue()
        self.complete_quest()
        self.get_rid_of_completed_quests()

    def complete_quest(self):
        if self.player.current_amount >= self.player.max_amount:
            self.player.completed_quests.append(self.player.current_quest)
            self.player.exp += quest_data[self.player.current_quest]['rewardXP']
            self.player.balance += quest_data[self.player.current_quest]['rewardMoney']
            self.player.current_quest = -1
            self.player.quest_accepted = False
            self.player.current_amount = 0

    def accept_quest(self):
        if not self.quest_accepted and self.player.current_quest == -1:
            self.player.current_quest = self.quests[0]
            self.player.max_amount = quest_data[self.quests[0]]['max_amount']
            self.player.quest_accepted = True

    def get_rid_of_completed_quests(self):
        for quest in self.player.completed_quests:
            if quest in self.quests:
                self.quests.remove(quest)

    def show_dialogue(self):
        if self.toggle_dialogue and self.range_of_player and self.quests != [] and self.player.current_quest == -1:
            self.dialogue.display(
                self.npc_name, str(quest_data[self.quests[0]]['text']))

            if self.dialogue.should_close_dialogue():
                self.toggle_dialogue = False

    def show_dialogue_button(self):
        if self.quests != [] and self.player.current_quest == -1 and self.range_of_player and not self.toggle_dialogue:
            self.dialogue.display_dialogue_button()
