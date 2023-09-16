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
from world.world_grass import get_dict


class World(Level):
    def __init__(self, change_level):
        super().__init__()

        self.change_level = change_level
        self.animation_stop = False
        self.map_image = pygame.image.load(
            'new_map/MSmap_background.png').convert_alpha()

        self.animation = Animation()

    def run(self, visible_sprites, obstacle_sprites, player):
        if not self.animation_stop:
            self.animation.update(visible_sprites, obstacle_sprites)
        self.show_map(player)
        self.input()
        self.cooldowns()

    def create_map(self, visible_sprites, obstacle_sprites, attackable_sprites, player_completed_quests, difficulty_level, trigger_death_particles, spawn_projectile, questgivers_quest_setup):

        layouts = {
            'boundary': import_csv_layout('new_map/MSmap._walls.csv'),
            'grass': import_csv_layout('new_map/MSmap._grass.csv'),
            'object': import_csv_layout('new_map/MSmap._objects.csv'),
            'entities': import_csv_layout('new_map/MSmap._entities.csv'),
            'dungeonportals': import_csv_layout('new_map/MSmap._dungeonentrance.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'object': import_folder_sorted('graphics/objects'),
        }

        dict_layouts = {
            'grass': get_dict('world_grass_data')}

        for dict_layout in dict_layouts.values():
            for tile in dict_layout:
                x = tile['j'] * Settings.TILESIZE
                y = tile['i'] * Settings.TILESIZE
                if tile['value'] != -1:
                    random_grass_image = choice(graphics['grass'])
                    tile = Tile((x, y), [visible_sprites,
                                         obstacle_sprites, attackable_sprites], 'grass', random_grass_image)
                    self.grass_tiles.append(tile)

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * Settings.TILESIZE
                        y = row_index * Settings.TILESIZE
                        if style == 'boundary':
                            tile = Tile((x, y), [obstacle_sprites],
                                        'invisible', pygame.Surface(
                                            (Settings.TILESIZE, Settings.TILESIZE)))

                        # if style == 'grass':
                        #     random_grass_image = choice(graphics['grass'])
                        #     tile = Tile((x, y), [visible_sprites,
                        #                          obstacle_sprites, attackable_sprites], 'grass', random_grass_image)
                        #     self.grass_tiles.append(tile)

                        if style == 'dungeonportals':
                            if col == '178':
                                surf = graphics['object'][int(col)]
                                tile = Tile((x, y+64), [visible_sprites,
                                                        obstacle_sprites], 'dungeonportals', surf)
                                self.dungeon_entrances.append(tile)

                        if style == 'object':
                            surf = graphics['object'][int(col)]
                            tile = Tile((x, y+64), [visible_sprites,
                                                    obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '59':
                                self.create_npc(
                                    col, x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)

                            elif col == '79':
                                self.create_npc(
                                    col, x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)

                            elif col == '139':
                                self.create_npc(
                                    col, x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)

                            elif col == '99':
                                self.create_npc(
                                    col, x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)

                            elif col == '119':
                                self.create_npc(
                                    col, x, y, Settings.npc_data, visible_sprites, obstacle_sprites, questgivers_quest_setup)

                            else:
                                passSpawn = False
                                if col == '18':
                                    monster_name = 'skeleton'
                                elif col == '38':
                                    if 6 not in player_completed_quests:
                                        monster_name = 'crab'
                                elif col == '58':
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

    # def restart_level(self):

    #         questgiver.load_quests()

    #     self.kill_all_enemies()

    #     self.spawn_enemies()
    #     self.spawn_grass()

    # def kill_all_enemies(self):
    #     for enemy in self.enemy_sprites:
    #         enemy.kill()

    # def spawn_grass(self):
    #     self.layouts = {
    #         'grass': import_csv_layout('new_map/MSmap._grass.csv'),
    #     }
    #     self.graphics = {
    #         'grass': import_folder('self.graphics/grass'),
    #     }

    #     for style, layout in self.layouts.items():
    #         for row_index, row in enumerate(layout):
    #             for col_index, col in enumerate(row):
    #                 if col != '-1':
    #                     x = col_index * Settings.TILESIZE
    #                     y = row_index * Settings.TILESIZE

    #                     if not self.tile_exists_at_position(x, y, 'grass'):
    #                         if style == 'grass':
    #                             random_grass_image = choice(
    #                                 self.graphics['grass'])
    #                             Tile((x, y), [visible_sprites,
    #                                           obstacle_sprites, attackable_sprites], 'grass', random_grass_image)

    # def tile_exists_at_position(self, x, y, sprite_type):
    #     for tile in self.grass_tiles:
    #         if tile.sprite_type == sprite_type and tile.rect.x == x and tile.rect.y == y:
    #             return True
    #     return False

    # def spawn_enemies(self):
    #     self.layouts = {
    #         'entities': import_csv_layout('new_map/MSmap._entities.csv'),
    #     }

    #     for style, layout in self.layouts.items():
    #         for row_index, row in enumerate(layout):
    #             for col_index, col in enumerate(row):
    #                 if col != '-1':
    #                     x = col_index * Settings.TILESIZE
    #                     y = row_index * Settings.TILESIZE
    #                     if style == 'entities':
    #                         passSpawn = False
    #                         if col == '18':
    #                             monster_name = 'skeleton'
    #                         elif col == '38':
    #                             monster_name = 'crab'
    #                         elif col == '58':
    #                             monster_name = 'wizzard'
    #                         else:
    #                             passSpawn = True
    #                         if not passSpawn:
    #                             enemy = Enemy(monster_name, (x, y), [
    #                                 visible_sprites, attackable_sprites], obstacle_sprites,
    #                                 self.trigger_death_particles, self.drop_loot, self.spawn_projectile, self.level)
    #                             self.enemy_sprites.append(enemy)

    # def teleport_to_dungeon(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_e] and not self.is_key_pressed:
    #         if self.player.in_range_of_dungeon_portal and not self.player.is_inside_dungeon and self.player.current_quest == 7:
    #             self.dungeon = self.create_dungeon()
    #             self.player.hitbox.center = self.dungeon_spawn[self.dungeon_id].rect.center
    #             self.player.is_inside_dungeon = True

    #             self.is_key_pressed = True
    #             self.key_press_time = pygame.time.get_ticks()

    #         elif self.player.in_range_of_dungeon_portal and self.player.is_inside_dungeon:
    #             self.player.hitbox.center = self.dungeon_entrances[self.dungeon_id].rect.center
    #             self.dungeon.empty()
    #             self.dungeon = None
    #             self.player.is_inside_dungeon = False

    #             self.is_key_pressed = True
    #             self.key_press_time = pygame.time.get_ticks()

    # def is_player_in_range_of_dungeon_portal(self):
    #     if not self.player.is_inside_dungeon:
    #         for dungeon in self.dungeon_entrances:
    #             player_pos = self.player.rect.center
    #             distance = pygame.math.Vector2(
    #                 (dungeon.x, dungeon.y)) - player_pos
    #             if distance.length() <= 100:
    #                 self.player.in_range_of_dungeon_portal = True
    #                 self.dungeon_id = self.dungeon_entrances.index(dungeon)
    #                 self.ui.display_dungeon_portal_text()
    #             else:
    #                 self.player.in_range_of_dungeon_portal = False
    #     else:
    #         for dungeon in self.dungeon_exits:
    #             player_pos = self.player.rect.center
    #             distance = pygame.math.Vector2(
    #                 (dungeon.x, dungeon.y)) - player_pos
    #             if distance.length() <= 100:
    #                 self.player.in_range_of_dungeon_portal = True
    #             else:
    #                 self.player.in_range_of_dungeon_portal = False
