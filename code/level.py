from PIL import Image, ImageDraw
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
import random
import math
from menuenums import menuenums
from animation import Animation
from questgiver import QuestGiver
from merchant import Merchant
from projectile import Projectile
from settings import Settings


class Level:
    def __init__(self, save):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        self.save = save

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.dungeon_entrances = []
        self.dungeon_exits = []
        self.dungeon_spawns = []
        self.dungeon_id = None

        # sprite setup
        self.create_map()
        # attack sprites
        self.current_attack = None

        # UI
        self.ui = UI()
        self.talents = Talents(self.player)
        self.game_paused = False
        self.menu_type = None

        self.key_press_time = None
        self.key_press_cooldown = 500
        self.is_key_pressed = False

        # particles
        self.particle_player = AnimationPlayer()

        self.loots = []

        self.animation = Animation()

        self.minimap_image = pygame.image.load(
            'new_map/minimap_background.png')
        self.is_minimap_open = False

        self.game_start_time = pygame.time.get_ticks()
        self.game_time = 0
        self.reset_interval = 24 * 60 * 60 * 1000

    def create_map(self):
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

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * Settings.TILESIZE
                        y = row_index * Settings.TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites],
                                 'invisible', pygame.Surface(
                                     (Settings.TILESIZE, Settings.TILESIZE)))
                        if style == 'grass':
                            random_grass_image = choice(
                                graphics['grass'])
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites, self.attackable_sprites], 'grass', random_grass_image)

                        if style == 'dungeonportals':

                            if col == '178':
                                surf = graphics['object'][int(col)]
                                self.dungeon_entrances.append(Tile((x, y+64), [self.visible_sprites,
                                                                               self.obstacle_sprites], 'dungeonportals', surf))
                        if style == 'object':
                            # create object tile
                            surf = graphics['object'][int(col)]

                            Tile((x, y+64), [self.visible_sprites,
                                             self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '39':
                                if self.save[0] == "existing":
                                    self.player = Player(
                                        self.save[1]['player_pos'], [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.save[1], None)
                                else:
                                    self.player = Player(
                                        (x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.save[1], "newCharacter")

                            elif col == '59':
                                self.create_npc(
                                    col, x, y, Settings.npc_data)
                            elif col == '79':
                                self.create_npc(
                                    col, x, y, Settings.npc_data)
                            elif col == '139':
                                self.create_npc(
                                    col, x, y, Settings.npc_data)
                            elif col == '99':
                                self.create_npc(
                                    col, x, y, Settings.npc_data)
                            elif col == '119':
                                self.create_npc(
                                    col, x, y, Settings.npc_data)

                            else:
                                if col == '18':
                                    monster_name = 'skeleton'
                                elif col == '38':
                                    monster_name = 'crab'
                                elif col == '58':
                                    monster_name = 'wizzard'
                                else:
                                    monster_name = 'squid'

                                Enemy(monster_name, (x, y), [
                                      self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                                      self.trigger_death_particles, self.update_quest_progress, self.drop_loot, self.spawn_projectile)

    def create_dungeon(self):
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
                        x = (col_index * Settings.TILESIZE)-5000
                        y = (row_index * Settings.TILESIZE)-5000
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites],
                                 'invisible',  pygame.Surface(
                                (Settings.TILESIZE, Settings.TILESIZE)))
                        if style == 'object':
                            # create object tile
                            surf = graphics['object'][int(col)]

                            Tile((x, y+64), [self.visible_sprites,
                                             self.obstacle_sprites], 'object', surf)

                        if style == 'dungeonportals':

                            if col == '178':
                                surf = graphics['object'][int(col)]
                                self.dungeon_exits.append(Tile((x, y), [self.visible_sprites,
                                                                        self.obstacle_sprites], 'dungeonportals', surf))
                            if col == '179':
                                surf = graphics['object'][int(col)]
                                self.dungeon_spawns.append(Tile((x, y), [self.visible_sprites,
                                                                         self.obstacle_sprites], 'dungeonportals', surf))

                        if style == 'entities':
                            if col == '18':
                                monster_name = 'skeleton'
                            elif col == '38':
                                monster_name = 'crab'
                            elif col == '58':
                                monster_name = 'wizzard'
                            else:
                                monster_name = 'squid'

                            enemy = Enemy(monster_name, (x, y), [
                                self.visible_sprites, self.attackable_sprites], self.obstacle_sprites,
                                self.trigger_death_particles, self.update_quest_progress, self.drop_loot, self.spawn_projectile)
                            # Add the enemy to the dungeon sprite group
                            dungeon_sprites.add(enemy)

        return dungeon_sprites  # Return the dungeon sprite group

    def is_player_in_range_of_dungeon_portal(self):
        if not self.player.is_inside_dungeon:
            for dungeon in self.dungeon_entrances:
                player_pos = self.player.rect.center
                distance = pygame.math.Vector2(
                    (dungeon.x, dungeon.y)) - player_pos
                if distance.length() <= 100:
                    self.player.in_range_of_dungeon_portal = True
                    self.dungeon_id = self.dungeon_entrances.index(dungeon)
                else:
                    self.player.in_range_of_dungeon_portal = False
        else:
            for dungeon in self.dungeon_exits:
                player_pos = self.player.rect.center
                distance = pygame.math.Vector2(
                    (dungeon.x, dungeon.y)) - player_pos
                if distance.length() <= 100:
                    self.player.in_range_of_dungeon_portal = True
                else:
                    self.player.in_range_of_dungeon_portal = False

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.is_key_pressed:
            if current_time - self.key_press_time >= self.key_press_cooldown:
                self.is_key_pressed = False

    def teleport_to_dungeon(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and not self.is_key_pressed:
            if self.player.in_range_of_dungeon_portal and not self.player.is_inside_dungeon:
                self.dungeon = self.create_dungeon()
                self.player.hitbox.center = self.dungeon_spawns[self.dungeon_id].rect.center
                self.player.is_inside_dungeon = True

                self.is_key_pressed = True
                self.key_press_time = pygame.time.get_ticks()

            elif self.player.in_range_of_dungeon_portal and self.player.is_inside_dungeon:
                self.player.hitbox.center = self.dungeon_entrances[self.dungeon_id].rect.center
                self.dungeon.empty()  # Empty the dungeon sprite group
                self.dungeon = None  # Set the dungeon object to None
                self.player.is_inside_dungeon = False

                self.is_key_pressed = True
                self.key_press_time = pygame.time.get_ticks()

    def drop_loot(self, x, y, monster_name):
        x += random.randint(-100, 100)
        y += random.randint(-100, 100)
        loot_types = list(Settings.monster_data[monster_name]['loots'])

        # Exclude xp_orb from the loot_types list
        loot_types.remove('xp_orb')

        # Check if there should be a drop or not for other loot types
        no_drop_chance = 0  # Adjust the chance as desired

        # Determine whether to drop xp_orb or not
        drop_xp_orb = random.random() >= no_drop_chance

        if drop_xp_orb:
            xp_orb_amount = Settings.monster_data[monster_name]['exp']
            self.loots.append(("xp_orb", xp_orb_amount, (x, y)))

        # Drop other loot types
        for loot_type in loot_types:
            chance = Settings.loots[loot_type]['chance']
            if random.random() < chance:
                loot_amount = Settings.loots[loot_type]['amount']
                loot_x = x
                loot_y = y

                # Generate separate position for items
                if drop_xp_orb:
                    loot_x += random.randint(-50, 50)
                    loot_y += random.randint(-50, 50)

                self.loots.append((loot_type, loot_amount, (loot_x, loot_y)))

    def draw_and_collect_loot(self, player):
        player_x, player_y = player.rect.center
        collected_loot = []

        for loot_type, loot_amount, loot_pos in self.loots:
            loot_x, loot_y = loot_pos
            loot_offset_x = loot_x - player_x + Settings.WIDTH // 2
            loot_offset_y = loot_y - player_y + Settings.HEIGHT // 2

            loot_graphics = Settings.loots[loot_type]['graphics']
            loot_image = pygame.image.load(loot_graphics)
            loot_rect = loot_image.get_rect(
                center=(loot_offset_x, loot_offset_y))

            # Calculate vertical animation position
            distance = math.sqrt((player_x - loot_x) **
                                 2 + (player_y - loot_y) ** 2)

            self.display_surface.blit(loot_image, loot_rect)

            if distance < 90:
                collected_loot.append((loot_type, loot_amount, loot_pos))

        for loot in collected_loot:
            loot_type, loot_amount, loot_pos = loot
            if loot_type == 'gold_coin' or loot_type == 'gold_coins':
                player.balance += loot_amount
            elif loot_type == 'xp_orb':
                player.update_experience(loot_amount)
            self.loots.remove(loot)

    def create_npc(self, id, x, y, npc_data):
        if Settings.npc_data[id]['type'] == 'quest_giver':
            self.npc = QuestGiver(npc_data[id]['name'], (x, y), [
                self.visible_sprites], self.obstacle_sprites, npc_data[id]['quest_ids'], id,)
        elif Settings.npc_data[id]['type'] == 'merchant':
            self.npc = Merchant(npc_data[id]['name'], (x, y), [
                self.visible_sprites], self.obstacle_sprites, id, npc_data[id]['item_list'])

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
                            if target_sprite.vulnerable:
                                self.particle_player.display_damage_numbers(target_sprite.rect.midtop, [
                                    self.visible_sprites], self.player.get_full_damage())
                            target_sprite.get_damage(
                                self.player, attack_sprite.sprite_type)

    def trigger_death_particles(self, pos, particle_type):
        self.particle_player.create_particles(particle_type, pos, [
                                              self.visible_sprites])

    def spawn_projectile(self, begin_pos, end_pos, projectile_tpye):
        self.projectile = Projectile(
            [self.visible_sprites], begin_pos, end_pos, projectile_tpye)

    def update_quest_progress(self, player):
        if player.current_quest != -1:
            if player.current_amount < player.max_amount:
                player.current_amount += 1

    def toggle_menu(self, menu_type):
        self.menu_type = menu_type
        self.game_paused = not self.game_paused

    def night_lights(self):

        if 1080 <= self.game_time < 1440:
            center_x = Settings.WIDTH // 2
            center_y = Settings.HEIGHT // 2
            radius = min(center_x, center_y) + 700 - \
                (math.sin(pygame.time.get_ticks() / 300) * 20)
            border_width = 1000
            color = (0, 0, 0, 222)

            # Create a new Surface with the appropriate dimensions to draw the circle
            circle_surface = pygame.Surface(
                (Settings.WIDTH, Settings.HEIGHT), pygame.SRCALPHA)

            circle_surface.set_alpha(220)
            # Border size

            pygame.draw.circle(circle_surface, color,
                               (center_x, center_y), radius, border_width)

            # Now, blit (draw) the circle_surface onto your display_surface
            self.display_surface.blit(circle_surface, (0, 0))

    def show_minimap(self, player):
        if self.is_minimap_open:
            # Calculate the scaling factor to fit the minimap on the screen (adjust as needed)
            scale_factor = 0.13

            # Calculate the size of the minimap
            minimap_width = int(self.minimap_image.get_width() * scale_factor)
            minimap_height = int(
                self.minimap_image.get_height() * scale_factor)

            # Create a new surface for the border
            border_surface = pygame.Surface(
                (minimap_width + 10, minimap_height + 10))

            # Draw a rectangle on the border surface for the border
            border_rect = pygame.Rect(
                0, 0, minimap_width + 10, minimap_height + 10)
            pygame.draw.rect(
                border_surface, Settings.MENU_BORDER_COLOR, border_rect)

            # Create a new surface for the minimap
            minimap = pygame.Surface((minimap_width, minimap_height))

            # Scale the full image onto the minimap
            minimap.blit(pygame.transform.scale(self.minimap_image,
                         (minimap_width, minimap_height)), (0, 0))

            # Calculate the player's position on the minimap using the rect attribute
            player_pos_x = int(player.rect.centerx * scale_factor)
            player_pos_y = int(player.rect.centery * scale_factor)

            # Draw a red dot for the player's position on the minimap
            dot_radius = 3
            pygame.draw.circle(minimap, (255, 0, 0),
                               (player_pos_x, player_pos_y), dot_radius)

            # Blit the minimap onto the border surface with an offset for the border
            border_surface.blit(minimap, (5, 5))

            # Show the border with the minimap on the screen
            border_x = Settings.WIDTH / 2 - border_surface.get_width() / 2
            border_y = 50
            self.display_surface.blit(border_surface, (border_x, border_y))

    def count_time(self):
        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # Calculate the elapsed time since the game started in milliseconds
        elapsed_time = current_time - self.game_start_time

        # Convert elapsed_time to seconds and add to the game_time
        self.game_time = elapsed_time / 1000

        # Reset the game_start_time if 24 minutes have passed
        if elapsed_time >= self.reset_interval:
            self.game_start_time = current_time
            self.game_time = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_m]:
            self.is_minimap_open = not self.is_minimap_open

    def run(self):
        self.visible_sprites.custom_draw(self.player)

        if self.game_paused:
            if self.menu_type == menuenums.TALENTS:
                self.talents.display()
        else:
            self.cooldowns()
            self.animation.update(self.visible_sprites, self.obstacle_sprites)
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.visible_sprites.npc_update(self.player)
            self.visible_sprites.projectile_update(self.player)
            if self.current_attack:
                self.current_attack.update()
            self.player_attack_logic()
            self.draw_and_collect_loot(self.player)
            self.is_player_in_range_of_dungeon_portal()
            self.teleport_to_dungeon()
            self.night_lights()
            self.input()
            self.count_time()
            self.show_minimap(self.player)
        self.ui.display(self.player)


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

        self.dungeon0_surf = pygame.image.load(
            'dungeontest\dungeontest.png').convert()
        self.dungeon0_rect = self.dungeon0_surf.get_rect(
            topleft=(-5000, -5000))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        dungeon0_offset_pos = self.dungeon0_rect.topleft - self.offset
        self.display_surface.blit(self.dungeon0_surf, dungeon0_offset_pos)

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

    def projectile_update(self, player):
        projectile_sprites = [sprite for sprite in self.sprites()if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'projectile']
        for projectile in projectile_sprites:
            projectile.update_projectile(player)
