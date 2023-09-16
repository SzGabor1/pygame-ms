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
        layouts = {
            'boundary': import_csv_layout('dungeontest/dungeontest_walls.csv'),
            'object': import_csv_layout('dungeontest/dungeontest_objects.csv'),
            'entities': import_csv_layout('dungeontest/dungeontest_entities.csv'),
            'dungeonportals': import_csv_layout('dungeontest/dungeontest_dungeonportals.csv'),
        }
        graphics = {
            'object': import_folder_sorted('graphics/objects'),
        }

        # Create a sprite group for the dungeon
        dungeon_sprites = pygame.sprite.Group()

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = (col_index * Settings.TILESIZE)
                        y = (row_index * Settings.TILESIZE)
                        if style == 'boundary':
                            Tile((x, y), [obstacle_sprites],
                                 'invisible',  pygame.Surface(
                                (Settings.TILESIZE, Settings.TILESIZE)))
                        if style == 'object':
                            # create object tile
                            surf = graphics['object'][int(col)]

                            Tile((x, y+64), [visible_sprites,
                                             obstacle_sprites], 'object', surf)

                        if style == 'dungeonportals':

                            if col == '178':
                                surf = graphics['object'][int(col)]
                                self.dungeon_exits.append(Tile((x, y), [visible_sprites,
                                                                        obstacle_sprites], 'dungeonportals', surf))
                            if col == '179':
                                surf = graphics['object'][int(col)]
                                self.dungeon_spawn.append(Tile(
                                    (x, y), [visible_sprites, obstacle_sprites], 'dungeonportals', surf))

                        if style == 'entities':
                            if col == '18':
                                monster_name = 'skeleton'
                            elif col == '38':
                                monster_name = 'crab'
                            elif col == '58':
                                monster_name = 'wizzard'
                            else:
                                monster_name = 'skeleton'

                            self.enemy_sprites = Enemy(monster_name, (x, y), [
                                visible_sprites, attackable_sprites], obstacle_sprites,
                                trigger_death_particles, self.drop_loot, spawn_projectile, difficulty_level)

        return dungeon_sprites
