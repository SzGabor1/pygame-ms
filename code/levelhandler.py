import pygame
from projectile import Projectile
from world import World
from support import import_csv_layout
from settings import Settings
from player import Player
from weapon import Weapon
from particles import AnimationPlayer
from menuenums import levelstates
from dungeon import Dungeon
from debug import debug


class LevelHandler():
    def __init__(self, load_data):
        self.load_data = load_data
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        self.particle_player = AnimationPlayer()

        self.load_difficulty_level(load_data)

        self.create_player()

        self.state = levelstates.WORLD
        if self.state == levelstates.WORLD:
            self.create_world()
            self.visible_sprites.floor_surf = self.world.map_image
        elif self.state == levelstates.DUNGEON:
            self.create_dungeon()
            self.visible_sprites.floor_surf = self.dungeon.dungeon_image

    def change_level(self, level):
        self.state = level

        # Kill all sprites except the player
        for sprite in self.visible_sprites.sprites():
            if sprite != self.player:
                sprite.kill()

        for sprite in self.obstacle_sprites.sprites():
            if sprite != self.player:
                sprite.kill()

        for sprite in self.attack_sprites.sprites():
            if sprite != self.player:
                sprite.kill()

        for sprite in self.attackable_sprites.sprites():
            if sprite != self.player:
                sprite.kill()

        # Create the new level environment based on the state
        if self.state == levelstates.WORLD:
            self.create_world()
            self.visible_sprites.floor_surf = self.world.map_image
        elif self.state == levelstates.DUNGEON:
            self.create_dungeon()
            self.visible_sprites.floor_surf = self.dungeon.dungeon_image

    def is_player_in_range_of_dungeon_portal(self):
        if not self.player.is_inside_dungeon:
            for dungeon in self.world.dungeon_entrances:
                player_pos = self.player.rect.center
                distance = pygame.math.Vector2(
                    (dungeon.x, dungeon.y)) - player_pos
                if distance.length() <= 100:
                    self.player.in_range_of_dungeon_portal = True
                    self.dungeon_id = self.world.dungeon_entrances.index(
                        dungeon)
                else:
                    self.player.in_range_of_dungeon_portal = False
        else:
            for dungeon in self.dungeon.dungeon_exits:
                player_pos = self.player.rect.center
                distance = pygame.math.Vector2(
                    (dungeon.x, dungeon.y)) - player_pos
                if distance.length() <= 100:
                    self.player.in_range_of_dungeon_portal = True
                else:
                    self.player.in_range_of_dungeon_portal = False

    def teleport_to_dungeon(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:

            if self.player.in_range_of_dungeon_portal and not self.player.is_inside_dungeon and self.player.current_quest == 7:
                self.change_level(levelstates.DUNGEON)
                self.player.hitbox.center = self.dungeon.dungeon_spawn[self.dungeon_id].rect.center
                self.player.is_inside_dungeon = True

               # self.is_key_pressed = True
                #self.key_press_time = pygame.time.get_ticks()

            elif self.player.in_range_of_dungeon_portal and self.player.is_inside_dungeon:
                self.change_level(levelstates.WORLD)
                self.player.hitbox.center = self.world.dungeon_entrances[self.dungeon_id].rect.center
                self.player.is_inside_dungeon = False

                #self.is_key_pressed = True
                #self.key_press_time = pygame.time.get_ticks()

    def create_world(self):
        self.world = World(self.change_level)
        self.world.create_map(self.visible_sprites,
                              self.obstacle_sprites, self.attackable_sprites, self.player.completed_quests, self.difficulty_level, self.trigger_death_particles, self.spawn_projectile, self.questgivers_quest_setup)
        print("quests removed")
        self.questgivers_quest_setup()

        print("world created")
        self.is_all_quests_completed()

    def create_dungeon(self):
        self.dungeon = Dungeon(self.change_level)
        self.dungeon.create_dungeon(self.visible_sprites,
                                    self.obstacle_sprites, self.attackable_sprites, self.player.completed_quests, self.difficulty_level, self.trigger_death_particles, self.spawn_projectile)

    def questgivers_quest_setup(self):

        for questgiver in self.world.quest_givers:
            questgiver.get_rid_of_completed_quests(
                self.player.completed_quests)

    def load_difficulty_level(self, load_data):
        if load_data[0] == 'online':
            self.difficulty_level = load_data[1]['level']
        else:
            self.difficulty_level = 0

    def trigger_death_particles(self, pos, particle_type):
        self.particle_player.create_particles(particle_type, pos, [
                                              self.visible_sprites])

    def spawn_projectile(self, begin_pos, end_pos, projectile_tpye):
        self.projectile = Projectile(
            [self.visible_sprites], begin_pos, end_pos, projectile_tpye)

    def create_attack(self):
        self.current_attack = Weapon(
            self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def is_all_quests_completed(self):
        if self.player.completed_quests != []:
            for questgiver in self.world.quest_givers:
                print(questgiver.name, questgiver.quests)
                if questgiver.quests != []:
                    "not all quests completed"
                    return False
            print("all quests completed")

            if self.player.difficulty == 1:
                self.difficulty_level += 1
                self.player.handle_new_level()

                for questgiver in self.world.quest_givers:
                    questgiver.load_quests()

                print(self.player.completed_quests)

            # reload world
        #    self.change_level(levelstates.WORLD)

    def run(self):
        self.visible_sprites.custom_draw(self.player)

      #  self.cooldowns()

        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.npc_update(self.player)
        self.visible_sprites.projectile_update(self.player)

        # only should work if world is loaded
        if self.state == levelstates.WORLD:
            self.world.run(self.visible_sprites,
                           self.obstacle_sprites, self.player)
            self.world.player_attack_logic(
                self.attack_sprites, self.attackable_sprites, self.visible_sprites, self.player)
        elif self.state == levelstates.DUNGEON:
            self.dungeon.run(self.visible_sprites,
                             self.obstacle_sprites, self.player)
            self.dungeon.player_attack_logic(
                self.attack_sprites, self.attackable_sprites, self.visible_sprites, self.player)
        # if self.current_attack:
        #    self.current_attack.update()
      #  self.player_attack_logic()
        # self.draw_and_collect_loot(self.player)
        self.is_player_in_range_of_dungeon_portal()
        self.teleport_to_dungeon()
      #  self.night_lights()
      #  self.input()
      #  self.count_time()
      #  self.show_map(self.player)
       # self.is_all_quests_completed()
        # self.ui.display(self.player)

    def create_player(self):
        layouts = {
            'entities': import_csv_layout('new_map/MSmap._entities.csv'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * Settings.TILESIZE
                        y = row_index * Settings.TILESIZE

                        if style == 'entities':
                            if col == '39':
                                if self.load_data[0] == "existing" or self.load_data[0] == "online":
                                    self.player = Player(
                                        self.load_data[1]['player_pos'], [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.load_data[1], None, (x, y), self.load_data[1]['difficulty'], self.is_all_quests_completed, self.questgivers_quest_setup)
                                else:
                                    self.player = Player(
                                        (x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.load_data[1], "newCharacter", (x, y), self.load_data[1]['difficulty'], self.is_all_quests_completed, self.questgivers_quest_setup)


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

        # dungeon0_offset_pos = self.dungeon0_rect.topleft - self.offset
        # self.display_surface.blit(self.dungeon0_surf, dungeon0_offset_pos)

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
            sprite, 'sprite_type') and (sprite.sprite_type == 'questgiver' or sprite.sprite_type == 'merchant')]
        for npc in npc_sprites:
            npc.npc_update(player)

    def projectile_update(self, player):
        projectile_sprites = [sprite for sprite in self.sprites()if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'projectile']
        for projectile in projectile_sprites:
            projectile.update_projectile(player)
