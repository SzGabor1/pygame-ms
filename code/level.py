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
import random
import math
from menuenums import menuenums
from animation import Animation
from questgiver import QuestGiver
from merchant import Merchant
from projectile import Projectile
from settings import Settings
from menuenums import levelstates


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        self.dungeon_entrances = []
        self.dungeon_exits = []
        self.dungeon_spawn = []
        self.dungeon_id = None

        self.enemy_sprites = []
        self.quest_givers = []
        self.grass_tiles = []

        self.map_open_time = None
        self.map_cooldown = 500

        # particles
        self.particle_player = AnimationPlayer()

        self.loots = []

        self.is_map_open = False
        self.is_map_able_to_open = True

        self.game_start_time = pygame.time.get_ticks()
        self.game_time = 0
        self.reset_interval = 24 * 60 * 60 * 1000

    def is_all_quests_completed(self):
        for questgiver in self.quest_givers:
            if questgiver.quests != []:
                return False
        print("all quests completed")

        if self.player.difficulty == 1:
            self.level += 1
            self.player.handle_new_level()

            # have to reload npc quest lists
            self.restart_level()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.is_map_able_to_open:
            if current_time - self.map_open_time >= self.map_cooldown:
                self.is_map_able_to_open = True

    def drop_loot(self, x, y, monster_name):
        x += random.randint(-100, 100)
        y += random.randint(-100, 100)
        loot_types = list(Settings.monster_data[monster_name]['loots'])

        loot_types.remove('xp_orb')

        # Check if there should be a drop or not for other loot types
        no_drop_chance = 0

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

            loot_graphics = Settings.loots[loot_type]['self.graphics']
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

    def player_attack_logic(self, attack_sprites, attackable_sprites, visible_sprites, player):
        if attack_sprites:
            for attack_sprite in attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.particle_player.create_grass_particles(
                                    pos-offset, [visible_sprites])
                            target_sprite.kill()
                            player.progress_quest('cut_grass')
                        else:
                            if target_sprite.vulnerable:
                                self.particle_player.display_damage_numbers(target_sprite.rect.midtop, [
                                    visible_sprites], player.get_full_damage())
                            target_sprite.get_damage(
                                player, attack_sprite.sprite_type)

    def night_lights(self):

        if 1080 <= self.game_time < 1440:
            center_x = Settings.WIDTH // 2
            center_y = Settings.HEIGHT // 2
            radius = min(center_x, center_y) + 700 - \
                (math.sin(pygame.time.get_ticks() / 300) * 20)
            border_width = 1000
            color = (0, 0, 0, 222)

            circle_surface = pygame.Surface(
                (Settings.WIDTH, Settings.HEIGHT), pygame.SRCALPHA)

            circle_surface.set_alpha(220)

            pygame.draw.circle(circle_surface, color,
                               (center_x, center_y), radius, border_width)

            self.display_surface.blit(circle_surface, (0, 0))

    def what_is_the_next_quest(self, player):
        if player.completed_quests == [] or player.completed_quests == [0]:
            return 0
        last_quest = player.completed_quests[-1]
        length_of_quest_data = len(Settings.quest_data)
        if last_quest < length_of_quest_data:
            next_quest = last_quest + 1
            return next_quest

    def next_quest_npc_position(self, player):
        next_quest = self.what_is_the_next_quest(player)
        for questgiver in self.quest_givers:
            if next_quest in questgiver.quests:
                return questgiver.rect.center
        return None

    def show_map(self, player):
        if self.is_map_open:
            scale_factor = 0.13

            map_width = int(self.map_image.get_width() * scale_factor)
            map_height = int(
                self.map_image.get_height() * scale_factor)

            border_surface = pygame.Surface(
                (map_width + 10, map_height + 10))
            border_rect = pygame.Rect(
                0, 0, map_width + 10, map_height + 10)
            pygame.draw.rect(
                border_surface, Settings.MENU_BORDER_COLOR, border_rect)

            map = pygame.Surface((map_width, map_height))
            map.blit(pygame.transform.scale(self.map_image,
                                            (map_width, map_height)), (0, 0))

            player_pos_x = int(player.rect.centerx * scale_factor)
            player_pos_y = int(player.rect.centery * scale_factor)

            dot_radius = 3
            pygame.draw.circle(map, (255, 0, 0),
                               (player_pos_x, player_pos_y), dot_radius)

            npc_position = self.next_quest_npc_position(player)
            if npc_position is not None:
                npc_pos_x = int(npc_position[0] * scale_factor)
                npc_pos_y = int(npc_position[1] * scale_factor)
                pygame.draw.circle(map, (255, 255, 0),
                                   (npc_pos_x, npc_pos_y), dot_radius)

            border_surface.blit(map, (5, 5))

            border_x = Settings.WIDTH / 2 - border_surface.get_width() / 2
            border_y = 50
            self.display_surface.blit(border_surface, (border_x, border_y))

    def count_time(self):

        current_time = pygame.time.get_ticks()

        elapsed_time = current_time - self.game_start_time

        self.game_time = elapsed_time / 1000

        if elapsed_time >= self.reset_interval:
            self.game_start_time = current_time
            self.game_time = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_m] and self.is_map_able_to_open:
            self.is_map_open = not self.is_map_open
            self.map_open_time = pygame.time.get_ticks()
            self.is_map_able_to_open = False

    # def run(self):
    #     self.visible_sprites.custom_draw(self.player)

    #     if self.game_paused:
    #         if self.menu_type == menuenums.TALENTS:
    #             self.talents.display()
    #     else:
    #         self.cooldowns()

    #         self.visible_sprites.update()
    #         self.visible_sprites.enemy_update(self.player)
    #         self.visible_sprites.npc_update(self.player)
    #         self.visible_sprites.projectile_update(self.player)
    #         if self.current_attack:
    #             self.current_attack.update()
    #         self.player_attack_logic()
    #         self.draw_and_collect_loot(self.player)
    #        # self.is_player_in_range_of_dungeon_portal()
    #        # self.teleport_to_dungeon()
    #         self.night_lights()
    #         self.input()
    #         self.count_time()
    #         self.show_map(self.player)
    #         self.is_all_quests_completed()
    #     self.ui.display(self.player)
