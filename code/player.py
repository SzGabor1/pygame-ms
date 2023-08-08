import pygame
from settings import *
from support import import_folder
from debug import debug
from entity import Entity
from inventory import Inventory
from sound import Sounds


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, save_datas, newGame, spawn_point, difficulty):
        super().__init__(groups)
        self.newGame = newGame
        self.name = save_datas['player_name']
        self.character_id = save_datas['skin_id']
        self.spawn_point = spawn_point
        self.save_datas = save_datas
        self.image = pygame.image.load(
            'graphics/Characters/players/'+str(self.character_id)+'/down_idle/down_idle.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6,
                                        Settings.HITBOX_OFFSET['player'])

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        self.difficulty = difficulty

        # movement
        self.speed = 2
        self.attacking = False
        self.attack_cooldown = 300
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.weapon_index = 1
        self.weapon = list(Settings.weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        self.can_switch_item = True
        self.item_switch_time = None
        self.switch_duration_cooldown = 200
        self.attack_direction = None

        # stats

        self.stats = None
        self.max_stats = {'health': 300,
                          'energy': 160, 'attack': 110, 'speed': 20}
        self.upgrade_cost = {'health': 100,
                             'energy': 600, 'attack': 140, 'speed': 60}
        self.health = None
        self.energy = None
        self.speed = None
        self.exp = None
        self.balance = None

        # quest
        # self.completed_quests = [2, 4, 6, 7]
        self.completed_quests = None
        self.current_quest = None
        self.current_amount = None
        self.max_amount = None
        self.is_quest_completed = False
        self.quest_completed_time = None
        self.quest_popup_duration = 5000

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerable_duration = 500

        # # import sound
        # self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
        # self.weapon_attack_sound.set_volume(0.1)

        # inventory
        self.inventory = Inventory()
        self.inventory_index = 0

        self.init_stats()

        self.can_use_item = True
        self.item_use_time = None
        self.item_usage_cooldown = 1000
        self.speed = self.stats['speed']
        # strength potion timer
        self.strength_potion_time = None
        self.used_strength_potion = False
        self.strength_potion_duration = Settings.items[2]['duration']*1000

        self.in_range_of_dungeon_portal = False
        self.is_inside_dungeon = False

        Player.level = 2

    def init_stats(self):
        if not self.newGame:
            self.stats = {'health': self.save_datas['player_stats']['health'], 'energy': self.save_datas['player_stats']
                          ['energy'], 'attack': self.save_datas['player_stats']['attack'], 'speed': self.save_datas['player_stats']['speed']}
            self.health = self.save_datas['player_health']
            self.energy = self.save_datas['player_energy']
            self.exp = self.save_datas['player_exp']
            self.balance = self.save_datas['balance']
            self.completed_quests = self.save_datas['player_completed_quests']
            self.current_quest = self.save_datas['player_current_quest']
            self.current_amount = self.save_datas['player_current_amount']
            self.max_amount = self.save_datas['player_max_amount']
            self.init_inventory_items(None)
        else:
            self.stats = {'health': 100, 'energy': 60,
                          'attack': 10, 'speed': 6}
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            self.speed = self.stats['speed']
            self.exp = 0
            self.balance = 0
            self.completed_quests = []
            self.current_quest = -1
            self.current_amount = 0
            self.max_amount = 1
            self.init_inventory_items("yes")

    def init_inventory_items(self, newCharacter):
        if not newCharacter:
            for item_id in self.save_datas['player_inventory_item_ids']:
                self.inventory.add_item(item_id)

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status+'_idle'

            if self.attacking:
                self.direction.x = 0
                self.direction.y = 0

                if not 'attack' in self.status:
                    if 'idle' in self.status:
                        # override idle
                        self.status = self.status.replace('idle', 'attack')
            else:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack', '')

    def import_player_assets(self):
        character_path = 'graphics/characters/players/' + \
            str(self.character_id)+'/'

        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [],
                           'up_idle': [], 'down_idle': [], 'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations:
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def use_strength_potion(self):
        if not self.used_strength_potion:
            self.strength_potion_time = pygame.time.get_ticks()
            self.used_strength_potion = True
            self.stats['attack'] += Settings.items[2]['amount']

    def input(self):
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if not self.attacking:
            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.attack_direction = self.direction
                Sounds.play('sword')

        if keys[pygame.K_e] and self.can_switch_item:
            self.can_switch_item = False
            self.item_switch_time = pygame.time.get_ticks()

            if self.weapon_index < len(list(Settings.weapon_data.keys()))-1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0
            self.weapon = list(Settings.weapon_data.keys())[
                self.weapon_index]
        # sprint
        if keys[pygame.K_LSHIFT]:
            self.speed = self.stats['speed']*1.5
        else:
            self.speed = self.stats['speed']

        # inventory
        if keys[pygame.K_1] and self.can_switch_item:
            self.can_switch_item = False
            self.item_switch_time = pygame.time.get_ticks()
            self.inventory_index = 0
        elif keys[pygame.K_2] and self.can_switch_item:
            self.can_switch_item = False
            self.item_switch_time = pygame.time.get_ticks()
            self.inventory_index = 1
        elif keys[pygame.K_3] and self.can_switch_item:
            self.can_switch_item = False
            self.item_switch_time = pygame.time.get_ticks()
            self.inventory_index = 2
        elif keys[pygame.K_4] and self.can_switch_item:
            self.can_switch_item = False
            self.item_switch_time = pygame.time.get_ticks()
            self.inventory_index = 3
        elif keys[pygame.K_5] and self.can_switch_item:
            self.can_switch_item = False
            self.item_switch_time = pygame.time.get_ticks()
            self.inventory_index = 4
        elif keys[pygame.K_q] and self.can_use_item:
            self.can_use_item = False
            self.item_use_time = pygame.time.get_ticks()

            self.inventory.use_item(self.inventory_index, self)

    def check_direction(self):
        # if the player changes direction, the attack will be destroyed
        if self.direction != self.attack_direction and self.direction != pygame.math.Vector2(0, 0):
            self.destroy_attack()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            self.check_direction()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_item:
            if current_time - self.item_switch_time >= self.switch_duration_cooldown:
                self.can_switch_item = True

        if not self.can_use_item:
            if current_time - self.item_use_time >= self.item_usage_cooldown:
                self.can_use_item = True

        if self.used_strength_potion:
            if current_time - self.strength_potion_time >= self.strength_potion_duration:
                self.stats['attack'] -= 20
                self.used_strength_potion = False

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerable_duration:
                self.vulnerable = True

        if self.is_quest_completed:
            if current_time - self.quest_completed_time >= self.quest_popup_duration:
                self.is_quest_completed = False
                self.current_quest = -1

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

            # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha_value = self.wave_value()
            self.image.set_alpha(alpha_value)
        else:
            self.image.set_alpha(255)

    def get_full_damage(self):
        return self.stats['attack'] + Settings.weapon_data[self.weapon]['damage']

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def get_damage(self, amount):
        if self.vulnerable:
            self.health -= amount
            self.hurt_time = pygame.time.get_ticks()
            self.vulnerable = False

        if self.health < 0:
            self.handle_death()

    def handle_death(self):

        if self.difficulty == 0:
            # self.print_death_text("You died!")
            self.hitbox.topleft = self.spawn_point
        else:

            #self.print_death_text("Game over!")
            # self.delete_save()
            pygame.quit()

    def update_experience(self, amount):
        self.exp += amount

    def update_balance(self, amount):
        self.balance += amount

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
