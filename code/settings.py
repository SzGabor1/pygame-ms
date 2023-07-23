import json
import pygame


class Settings:
    def __init__(self, data):
        self.WIDTH = data['settings']['WIDTH']
        self.HEIGHT = data['settings']['HEIGHT']
        self.FULLSCREEN = data['settings']['FULLSCREEN']

        self.RESOLUTIONS = [
            (800, 600),
            (1024, 768),
            (1280, 720),
            (1680, 950)
        ]

        self.FPS = 120
        self.TILESIZE = 64
        self.HITBOX_OFFSET = {
            'player': -20,
            'object': -40,
            'building': -40,
            'grass': -10,
            'invisible': 0,
            'water': 20,
            'dungeonportals': -64
        }

        self.SOUNDS = {
            'main': 'audio/main.mp3',
            'sword': 'audio/sword.wav',
            'potion': 'audio/potion.wav',
            'click': 'audio/click.mp3',
            'death': 'audio/death.wav',
            'hit': 'audio/hit.wav',
            'slash': 'audio/attack/slash.wav',
            'claw': 'audio/attack/claw.wav',
            'fireball': 'audio/attack/fireball.wav',
            'potion': 'audio/potion.wav',

        }

        self.map_animation_data = {
            '125': 'graphics/animated/tree1',
            '127': 'graphics/animated/tree2',
            '165': 'graphics/animated/tree3',
            '167': 'graphics/animated/tree4',
            '205': 'graphics/animated/tree5',
            '207': 'graphics/animated/tree6',
            '169': 'graphics/animated/tree7',
            '5': 'graphics/animated/sandwater_left_corner',
            '6': 'graphics/animated/sandwater',
            '7': 'graphics/animated/sandwater_rigth_corner',
            '28': 'graphics/animated/sandwater_left_small_corner',
            '88': 'graphics/animated/sandwater_left_small_static_corner',
            '29': 'graphics/animated/sandwater_right_small_corner',
            '89': 'graphics/animated/sandwater_right_small_static_corner',
            '0': 'graphics/animated/grasswater_left_corner',
            '1': 'graphics/animated/grasswater',
            '2': 'graphics/animated/grasswater_right_corner',
            '23': 'graphics/animated/grasswater_left_small_corner',
            '107': 'graphics/animated/grasswater_left_small_statictop_corner',
            '108': 'graphics/animated/grasswater_left_staticbottom_corner',
            '24': 'graphics/animated/grasswater_right_small_corner',
            '109': 'graphics/animated/grasswater_right_small_statictop_corner',
            '131': 'graphics/animated/grasswater_right_staticbottom_corner'
        }

        self.character_ids = ['0', '1']

        self.loots = {
            'gold_coin': {'chance': 0.8, 'graphics': 'graphics/items/gold_coin.png', 'amount': 1000},
            'gold_coins': {'chance': 0.2, 'graphics': 'graphics/items/gold_coins.png', 'amount': 5000},
            'xp_orb': {'chance': 0, 'graphics': 'graphics/items/xp_orb.png', 'amount': 0}
        }

        # enemy
        self.monster_data = {
            'squid': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
            'crab': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
            'wizzard': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'slash', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
            'skeleton': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 100, 'exp': 150, 'damage': 8, 'attack_type': 'fireball', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350}
        }

        self.projectile_data = {
            'void': {'frames': 'graphics/particles/void', 'speed': 10, 'damage': 40, },
        }

        # weapons
        self.weapon_data = {
            'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'graphics/weapons/sword/full.png'},
            'lance': {'cooldown': 400, 'damage': 300, 'graphic': 'graphics/weapons/lance/full.png'},
            'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'graphics/weapons/axe/full.png'},
            'rapier': {'cooldown': 50, 'damage': 8, 'graphic': 'graphics/weapons/rapier/full.png'},
            'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'graphics/weapons/sai/full.png'}}

        # MENU UI
        self.MENU_BORDER_COLOR = '#551C03'
        self.MENU_BG_COLOR = '#F9AA5E'
        self.MENU_BUTTON_BG_COLOR = '#EE7F26'

        self.INVENTORY_BG_COLOR = '#F9AA5E'
        self.INVENTORY_BORDER_COLOR = '#551C03'
        self.INVENTORY_SELECTED_BG_COLOR = '#c56307'

        # UI
        self.BAR_HEIGHT = 20
        self.HEALTH_BAR_WIDTH = 200
        self.ENERGY_BAR_WIDTH = 140
        self.ITEM_BOX_SIZE = 80
        self.UI_FONT = 'graphics/font/joystix.ttf'
        self.UI_FONT_SIZE = 18

        # general colors
        self.WATER_COLOR = '#71ddee'
        self.UI_BG_COLOR = '#222222'
        self.UI_BORDER_COLOR = '#111111'
        self.TEXT_COLOR = '#EEEEEE'

        # UI colors
        self.HEALTH_COLOR = 'red'
        self.ENERGY_COLOR = 'blue'

        # talent menu
        self.BLACK_TEXT_COLOR = '#111111'
        self.WHITE_TEXT_COLOR = '#EEEEEE'
        self.BAR_COLOR = '#EEEEEE'
        self.BAR_COLOR_SELECTED = '#111111'
        self.TALENT_BG_COLOR_SELECTED = '#EEEEEE'

        self.npc_data = {
            '59': {'name': 'Laci 59', 'skin': 'Villager1', 'quest_ids': [1], 'type': 'quest_giver', 'item_list': None},
            '79': {'name': 'Roli 79', 'skin': 'Villager1', 'quest_ids': [2], 'type': 'quest_giver', 'item_list': None},
            '119': {'name': 'Matyi 119', 'skin': 'Villager1', 'type': 'merchant', 'item_list': [0, 1, 2, 3, 4, 5]},
            '99': {'name': 'Kevin 99', 'skin': 'Villager1', 'quest_ids': [3], 'type': 'merchant', 'item_list': [1, 2]},
            '139': {'name': 'Mate 139 ', 'skin': 'Villager1', 'quest_ids': [0], 'type': 'quest_giver', 'item_list': None}
        }

        self.quest_data = {
            0: {
                "text": "Öld meg a szellemeket",
                "objective": "Ölj meg 3 szellemet",
                "max_amount": 3,
                "enemy_type": "spirit",
                "rewardMoney": 200,
                "rewardXP": 3010
            },

            1: {
                "text": "Öld meg a crabt",
                "objective": "Öld meg a crabt",
                "max_amount": 1,
                "enemy_type": "crab",
                "rewardMoney": 500,
                "rewardXP": 4000
            },

            2: {
                "text": "Kutass az elveszett város romjaiban",
                "objective": "Fedezd fel az elveszett város romjait",
                "max_amount": 1,
                "enemy_type": "spirit",
                "rewardMoney": 300,
                "rewardXP": 2500
            },

            3: {
                "text": "Harcold le a sárkányt",
                "objective": "Öld meg a hatalmas sárkányt",
                "max_amount": 1,
                "enemy_type": "",
                "rewardMoney": 1000,
                "rewardXP": 8000
            },

            4: {
                "text": "Szerezd vissza az elveszett varázskönyvet",
                "objective": "Keresd meg az elveszett varázskönyvet",
                "max_amount": 1,
                "enemy_type": "",
                "rewardMoney": 400,
                "rewardXP": 3500
            },

            5: {
                "text": "Teljesíts egy veszélyes küldetést",
                "objective": "Teljesíts egy veszélyes küldetést a kiképződ segítségével",
                "max_amount": 1,
                "enemy_type": "",
                "rewardMoney": 800,
                "rewardXP": 6000
            },

            6: {
                "text": "Keress meg egy rejtélyes tárgyat",
                "objective": "Találd meg a rejtélyes tárgyat",
                "max_amount": 1,
                "enemy_type": "",
                "rewardMoney": 600,
                "rewardXP": 4500
            },

            7: {
                "text": "Tisztítsd meg a mocsarat a szörnyektől",
                "objective": "Ölj meg 5 mocsári szörnyet",
                "max_amount": 5,
                "enemy_type": "",
                "rewardMoney": 300,
                "rewardXP": 2800
            }
        }

        self.items = {

            0: {
                "id": 0,
                "name": "Health Potion",
                "description": "Regenerate a small amount of health.",
                "type": "consumable",
                "effect": "health",
                "amount": 60,
                "duration": 0,
                "graphic": "graphics/items/health_potion.png",
                "cost": 1000
            },
            1: {
                "id": 1,
                "name": "Energy Potion",
                "description": "Restores a small amount of mana.",
                "type": "consumable",
                "effect": "energy",
                "amount": 30,
                "duration": 0,
                "graphic": "graphics/items/energy_potion.png",
                "cost": 1600
            },
            2: {
                "id": 2,
                "name": "Strength Potion",
                "description": "Temporarily increases your strength.",
                "type": "consumable",
                "effect": "strength",
                "amount": 10,
                "duration": 60,
                "graphic": "graphics/items/strength_potion.png",
                "cost": 2000
            },            3: {
                "id": 3,
                "name": "Strength Potion",
                "description": "Temporarily increases your strength.",
                "type": "consumable",
                "effect": "strength",
                "amount": 10,
                "duration": 60,
                "graphic": "graphics/items/strength_potion.png",
                "cost": 2000
            },            4: {
                "id": 4,
                "name": "Strength Potion",
                "description": "Temporarily increases your strength.",
                "type": "consumable",
                "effect": "strength",
                "amount": 10,
                "duration": 60,
                "graphic": "graphics/items/strength_potion.png",
                "cost": 2000
            },            5: {
                "id": 5,
                "name": "Strength Potion",
                "description": "Temporarily increases your strength.",
                "type": "consumable",
                "effect": "strength",
                "amount": 10,
                "duration": 60,
                "graphic": "graphics/items/strength_potion.png",
                "cost": 2000
            },
        }

    def overwrite_settings(self, WIDTH, HEIGHT, fullscreen):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.fullscreen = fullscreen
        print(self.fullscreen)
        dictionary = {
            "settings": {
                "WIDTH": self.WIDTH,
                "HEIGHT": self.HEIGHT,
                "FULLSCREEN": self.fullscreen
            }
        }
        json_object = json.dumps(dictionary, indent=4)
        with open("data/settings/settings.json", "w") as outfile:
            outfile.write(json_object)
