from typing import Any
import pygame
from entity import Entity
from support import *
from settings import *
from dialogue import Dialogue

# ha quest felvételnél tapasztalható lesz lag, akkor kell egy quest osztály és memóriába kell tárolni az adatokat.


class NPC(Entity):
    def __init__(self, npc_name, pos, groups, obstacle_sprites, quests, settings):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'npc'
        self.settings = settings
        # graphics setup
        self.import_graphics(npc_name)
        self.status = 'profile'
        self.image = self.animations[self.status][self.frame_index]

        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.npc_name = npc_name
        self.npc_pos = pos
        self.quests = quests

        # self.player interaction
        self.range_of_player = False
        self.toggle_dialogue = False
        self.dialogue = Dialogue(self.accepting_quest,
                                 self.toggle_dialogue, self.settings)
        self.quest_accepted = False
        self.accept_quest_bool = False

        self.display_surface = pygame.display.get_surface()

    def import_graphics(self, name):
        self.animations = {'profile': []}
        main_path = f'graphics/Characters/players/1/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.toggle_dialogue = True

    def in_range_of_player(self, player):
        player_pos = player.rect.center
        distance = pygame.math.Vector2(self.npc_pos) - player_pos
        if distance.length() <= 100:
            self.range_of_player = True
        else:
            self.range_of_player = False
            self.toggle_dialogue = False

    def update(self):
        self.input()

    def npc_update(self, player):
        self.complete_quest(player)
        self.get_rid_of_completed_quests(player)
        self.show_dialogue(player)
        self.in_range_of_player(player)
        self.show_dialogue_button(player)

        if self.accept_quest_bool:
            self.accept_quest(player)

    def complete_quest(self, player):
        if player.current_amount >= player.max_amount:
            player.is_quest_completed = True
            player.quest_completed_time = pygame.time.get_ticks()
            player.completed_quests.append(player.current_quest)
            player.exp += self.settings.quest_data[player.current_quest]['rewardXP']
            player.balance += self.settings.quest_data[player.current_quest]['rewardMoney']

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
            player.max_amount = self.settings.quest_data[self.quests[0]]['max_amount']
            player.quest_accepted = True
            self.accept_quest_bool = False

    def show_dialogue(self, player):
        if self.toggle_dialogue and self.range_of_player and self.quests != [] and player.current_quest == -1:
            self.dialogue.display(
                self.npc_name, str(self.settings.quest_data[self.quests[0]]['text']))

            if self.dialogue.should_close_dialogue():
                self.toggle_dialogue = False

    def show_dialogue_button(self, player):
        if self.quests != [] and player.current_quest == -1 and self.range_of_player and not self.toggle_dialogue:
            self.dialogue.display_dialogue_button()
