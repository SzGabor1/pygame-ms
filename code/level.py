import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from random import randint
from talents import Talents
from ingame_menu import IngameMenu
from npc import NPC


class Level:
    def __init__(self, settings):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        self.settings = settings

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # attack sprites
        self.current_attack = None

        # UI
        self.ui = UI(self.settings)
        self.talents = Talents(self.player, self.settings)
        self.ingame_menu = IngameMenu(self.settings, self.toggle_menu)
        self.game_paused = False
        self.menu_type = None

        # particles
        self.particle_player = AnimationPlayer()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('new_map/MSmap._walls.csv'),
            'grass': import_csv_layout('new_map/MSmap._grass.csv'),
            'object': import_csv_layout('new_map/MSmap._objects.csv'),
            'entities': import_csv_layout('new_map/MSmap._entities.csv'),
        }
        graphics = {
            'grass': import_folder('graphics/grass'),
            'object': import_folder('graphics/objects'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * self.settings.TILESIZE
                        y = row_index * self.settings.TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites],
                                 'invisible', self.settings, pygame.Surface(
                                     (self.settings.TILESIZE, self.settings.TILESIZE)))
                        if style == 'grass':
                            random_grass_image = choice(
                                graphics['grass'])
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites, self.attackable_sprites], 'grass', self.settings, random_grass_image)
                        if style == 'object':
                            # create object tile
                            print(col)
                            print(str(x) + " " + str(y))
                            surf = graphics['object'][int(col)]

                            Tile((x, y+64), [self.visible_sprites,
                                 self.obstacle_sprites], 'object', self.settings, surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.settings)

                            elif col == '256':
                                self.create_npc(
                                    col, x, y, self.settings.npc_data)
                            elif col == '-2147483254':
                                self.create_npc(
                                    col, x, y, self.settings.npc_data)
                            elif col == '257':
                                self.create_npc(
                                    col, x, y, self.settings.npc_data)
                            elif col == '258':
                                self.create_npc(
                                    col, x, y, self.settings.npc_data)
                            elif col == '259':
                                self.create_npc(
                                    col, x, y, self.settings.npc_data)

                            else:
                                if col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'

                                Enemy(monster_name, (x, y), [
                                      self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                                      self.trigger_death_particles, self.update_quest_progress, self.settings)

    def create_npc(self, id, x, y, npc_data):
        self.npc = NPC(npc_data[id]['name'], (x, y), [
            self.visible_sprites], self.obstacle_sprites, npc_data[id]['quest_ids'], self.settings)

    def create_attack(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.particle_player.create_grass_particles(
                                    pos-offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type)

            # spawn particles
    def trigger_death_particles(self, pos, particle_type):
        self.particle_player.create_particles(particle_type, pos, [
                                              self.visible_sprites])

    def update_quest_progress(self, player):
        if player.current_quest != -1:
            if player.current_amount < player.max_amount:
                player.current_amount += 1

    def toggle_menu(self, menu_type):
        self.menu_type = menu_type
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            if self.menu_type == 'talents':
                self.talents.display()
        if self.game_paused:
            if self.menu_type == 'ingame_menu':
                self.ingame_menu.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.npc_update(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() / 2
        self.half_height = self.display_surface.get_height() / 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load(
            'new_map/MSmap_background.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.y):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites()if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def npc_update(self, player):
        npc_sprites = [sprite for sprite in self.sprites()if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'npc']
        for npc in npc_sprites:
            npc.npc_update(player)
