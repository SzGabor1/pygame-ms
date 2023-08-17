import pygame
from settings import *
from entity import Entity
from support import *
import random
import math
from sound import Sounds


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, trigger_death_particles, update_quest_progress, drop_loot, spawn_projectile, stat_scale):
        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = Settings.monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        self.scale_stats(stat_scale)

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.trigger_death_particles = trigger_death_particles
        self.update_quest_progress = update_quest_progress
        self.drop_loot = drop_loot
        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        self.is_projectile_spawned = False
        self.spawn_projectile = spawn_projectile
        self.projectile_position = None
        self.projectile_time = None
        self.projectile_cooldown = 4000
        self.projectile = [0, 0]
        self.able_to_shoot = True

    def scale_stats(self, stat_scale):
        if stat_scale == 0:
            return

        for x in range(stat_scale):
            self.health *= 1.25
            self.exp *= 1.25
            self.speed *= 1.1
            self.attack_damage *= 1.1
            self.resistance *= 1.1

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.able_to_shoot = True
        else:
            self.status = 'idle'
            self.able_to_shoot = False

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            # self.damage_player(self.attack_damage, self.attack_type)
            player.get_damage(self.attack_damage)
            Sounds.play(self.attack_type)

        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            if attack_type == 'weapon':
                self.health -= player.get_full_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            Sounds.play('hit')

    def check_death(self, player):
        if self.health <= 0:
            # print position
            self.drop_loot(self.rect.centerx,
                           self.rect.centery, self.monster_name)
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            Sounds.play('death')
            if not player.current_quest == -1:
                if(self.monster_name == Settings.quest_data[player.current_quest]['enemy_type']):
                    self.update_quest_progress()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            # flicer
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
        if self.is_projectile_spawned:
            if current_time - self.projectile_time >= self.projectile_cooldown:
                self.is_projectile_spawned = False

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def trigger_spawn_projectile(self, player):
        if self.monster_name == 'wizzard' and self.health < 0.75 * Settings.monster_data[self.monster_name]['health'] and not self.is_projectile_spawned and self.able_to_shoot:
            self.spawn_projectile(
                self.rect.midleft, player.rect.center, 'void')

            self.is_projectile_spawned = True
            self.projectile_time = pygame.time.get_ticks()

    def enemy_update(self, player):
        self.check_death(player)
        self.trigger_spawn_projectile(player)
        self.get_status(player)
        self.actions(player)
