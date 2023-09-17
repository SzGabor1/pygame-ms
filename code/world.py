import sys

from enemy import Enemy
from player import Player
from random import choice
from tile import Tile
from settings import Settings
from support import import_csv_layout, import_folder, import_folder_sorted
from level import Level
from merchant import Merchant
from questgiver import QuestGiver
from animation import Animation
import pygame

from world_data import world_grass, world_dungeonentrance, world_objects, world_entities, world_walls


class World(Level):
    def __init__(self, change_level):
        super().__init__()

        self.change_level = change_level
        self.animation_stop = False
        self.map_image = pygame.image.load(
            'new_map/MSmap_background.png').convert_alpha()
        self.minimap_image = pygame.image.load(
            'new_map/map_background.png').convert_alpha()

        self.animation = Animation()

    def run(self, visible_sprites, obstacle_sprites, player):
        if not self.animation_stop:
            self.animation.update(visible_sprites, obstacle_sprites)
        self.show_map(player)
        self.input()
        self.cooldowns()

    def create_map(self, visible_sprites, obstacle_sprites, attackable_sprites, player_completed_quests, difficulty_level, trigger_death_particles, spawn_projectile, questgivers_quest_setup):
        graphics = {
            'grass': import_folder('graphics/grass'),
            'object': import_folder_sorted('graphics/objects'),
        }

        dict_layouts = {
            'grass': world_grass.world_grass,
            'dungeonportals': world_dungeonentrance.world_dungeonentrance,
            'object': world_objects.world_objects,
            'entities': world_entities.world_entities,
            'boundary': world_walls.world_walls,
        }

        for key, tile in dict_layouts.items():
            for datas in tile:
                x = datas['j'] * Settings.TILESIZE
                y = datas['i'] * Settings.TILESIZE

                if key == 'boundary':
                    tile = Tile((x, y), [obstacle_sprites], 'invisible', pygame.Surface(
                        (Settings.TILESIZE, Settings.TILESIZE)))
                elif key == 'grass':
                    random_grass_image = choice(graphics['grass'])
                    tile = Tile((x, y), [visible_sprites, obstacle_sprites,
                                attackable_sprites], 'grass', random_grass_image)
                    self.grass_tiles.append(tile)
                elif key == 'dungeonportals':
                    if datas['value'] == 178:
                        surf = graphics['object'][datas['value']]
                        tile = Tile((x, y), [visible_sprites,
                                             obstacle_sprites], 'dungeonportals', surf)
                        self.dungeon_entrances.append(tile)
                elif key == 'object':
                    surf = graphics['object'][datas['value']]
                    tile = Tile((x, y), [visible_sprites,
                                         obstacle_sprites], 'object', surf)
                elif key == 'entities':
                    if datas['value'] == 59:
                        self.create_npc(
                            str(datas['value']), x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)
                    elif datas['value'] == 79:
                        self.create_npc(
                            str(datas['value']), x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)
                    elif datas['value'] == 139:
                        self.create_npc(
                            str(datas['value']), x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)
                    elif datas['value'] == 99:
                        self.create_npc(
                            str(datas['value']), x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)
                    elif datas['value'] == 119:
                        self.create_npc(
                            str(datas['value']), x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)
                    else:
                        passSpawn = False
                        if datas['value'] == 18:
                            monster_name = 'skeleton'
                        elif datas['value'] == 38:
                            if 6 not in player_completed_quests:
                                monster_name = 'crab'
                        elif datas['value'] == 58:
                            monster_name = 'wizzard'
                        else:
                            passSpawn = True
                        if not passSpawn:
                            Enemy(monster_name, (x, y), [
                                visible_sprites, attackable_sprites], obstacle_sprites,
                                trigger_death_particles, self.drop_loot, spawn_projectile, difficulty_level)

    def create_npc(self, id, x, y, npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup):
        if Settings.npc_data[id]['type'] == 'quest_giver':
            self.npc = QuestGiver(npc_data[id]['name'], (x, y), [
                visible_sprites], obstacle_sprites, id, questgivers_quest_setup)
            self.quest_givers.append(self.npc)
        elif Settings.npc_data[id]['type'] == 'merchant':
            self.npc = Merchant(npc_data[id]['name'], (x, y), [
                visible_sprites], obstacle_sprites, id, npc_data[id]['item_list'])
