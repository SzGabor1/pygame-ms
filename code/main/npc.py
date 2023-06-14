from typing import Any
import pygame
from entity import Entity
from support import *
from dialogue import Dialogue


class NPC(Entity):
    def __init__(self, npc_name, pos, groups, obstacle_sprites):
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

        # stats
        self.npc_name = npc_name
        self.npc_pos = pos

        # player interaction
        self.quest_id = 1
        self.range_of_player = False
        self.toggle_dialogue = False
        self.dialogue = Dialogue()

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

    def in_range_of_player(self, player):
        player_pos = player.rect.center
        distance = pygame.math.Vector2(self.npc_pos) - player_pos
        if distance.length() <= 100:
            self.range_of_player = True
        else:
            self.range_of_player = False
            self.toggle_dialogue = False

    def update(self):
        self.dialogue.display_dialogue_button(
            self.range_of_player, self.toggle_dialogue)
        self.input()
        if self.toggle_dialogue and self.range_of_player:
            self.dialogue.display(self.npc_name, "XFGSDHGDFGHSRTERTGSGHSF")

    def npc_update(self, player):
        self.in_range_of_player(player)
