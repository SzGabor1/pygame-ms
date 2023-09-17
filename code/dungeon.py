from random import choice
import pygame
from enemy import Enemy
from questgiver import QuestGiver
from merchant import Merchant
from tile import Tile
from support import import_csv_layout, import_folder, import_folder_sorted
from animation import Animation
from settings import Settings
from level import Level
from dungeon_data import dungeon_dungeonportals, dungeon_objects, dungeon_entities


class Dungeon(Level):
    def __init__(self, change_level):
        super().__init__()

        self.change_level = change_level

        self.dungeon_image = pygame.image.load(
            'dungeontest\dungeontest.png').convert()

        self.animation = Animation()

    def run(self, visible_sprites, obstacle_sprites, player):
        pass

    def create_dungeon(self, visible_sprites, obstacle_sprites, attackable_sprites, player_completed_quests, difficulty_level, trigger_death_particles, spawn_projectile):
        graphics = {
            'object': import_folder_sorted('graphics/objects'),
        }

        dict_layouts = {
            'dungeonportals': dungeon_dungeonportals.dungeon_dungeonportals,
            'object': dungeon_objects.dungeon_objects,
            'entities': dungeon_entities.dungeon_entities,
        }

        for key, tile in dict_layouts.items():
            for datas in tile:
                x = datas['j'] * Settings.TILESIZE
                y = datas['i'] * Settings.TILESIZE
                if key == 'dungeonportals':
                    if datas['value'] == 178:
                        surf = graphics['object'][datas['value']]
                        self.dungeon_exits.append(Tile((x, y), [visible_sprites,
                                                                obstacle_sprites], 'dungeonportals', surf))

                    if datas['value'] == 179:
                        surf = graphics['object'][datas['value']]
                        self.dungeon_spawn.append(Tile(
                            (x, y), [visible_sprites, obstacle_sprites], 'dungeonportals', surf))

                elif key == 'object':
                    surf = graphics['object'][datas['value']]
                    tile = Tile((x, y-64), [visible_sprites,
                                            obstacle_sprites], 'object', surf)
                elif key == 'entities':
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
