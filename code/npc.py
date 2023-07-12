from typing import Any
import pygame
from entity import Entity
from support import *
from settings import *
from dialogue import Dialogue

# ha quest felvételnél tapasztalható lesz lag, akkor kell egy quest osztály és memóriába kell tárolni az adatokat.


class NPC(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites, settings, id):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'npc'
        self.settings = settings
        self.id = id
        # graphics setup
        self.import_graphics(self.settings.npc_data[id]['skin'])
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.name = name
        self.npc_pos = pos

        self.display_surface = pygame.display.get_surface()

    def import_graphics(self, skin):
        self.animations = {'idle': []}
        main_path = f'graphics/Characters/'+skin+'/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.toggle_dialogue = True
            self.toggle_shop = True

    def in_range_of_player(self, player):
        player_pos = player.rect.center
        distance = pygame.math.Vector2(self.npc_pos) - player_pos
        if distance.length() <= 100:
            self.range_of_player = True
        else:
            self.range_of_player = False
            self.toggle_dialogue = False
