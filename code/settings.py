import json
import pygame
from support import import_settings as import_settings


class Settings:

    data = import_settings('data/settings/settings.json')
    WIDTH = data['settings']['WIDTH']
    HEIGHT = data['settings']['HEIGHT']
    FULLSCREEN = data['settings']['FULLSCREEN']
    VOLUME = data['settings']['VOLUME']

    @staticmethod
    def overwrite_settings(width, height, fullscreen, volume):
        with open('data/settings/settings.json', 'r') as infile:
            existing_settings = json.load(infile)
            VOLUME = existing_settings['settings']['VOLUME'] if volume is None else volume

        dictionary = {
            'settings': {
                'WIDTH': width,
                'HEIGHT': height,
                'FULLSCREEN': fullscreen,
                'VOLUME': VOLUME
            }
        }
        json_object = json.dumps(dictionary, indent=4)
        with open('data/settings/settings.json', 'w') as outfile:
            outfile.write(json_object)

    @staticmethod
    def overwrite_volume(volume):
        Settings.VOLUME = volume
        # Update settings in the JSON file with the new volume value
        with open('data/settings/settings.json', 'r') as infile:
            data = json.load(infile)
            data['settings']['VOLUME'] = volume
        with open('data/settings/settings.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    FPS = 120
    TILESIZE = 64
    HITBOX_OFFSET = {
        'player': -20,
        'object': -40,
        'trees': -60,
        'building': -40,
        'grass': -10,
        'invisible': 0,
        'water': 20,
        'dungeonportals': -64,
        'borders': 20
    }

    SOUNDS = {
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

    map_animation_data = {
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

    character_ids = ['0', '1']

    loots = {
        'gold_coin': {'chance': 0.8, 'graphics': 'graphics/items/gold_coin.png', 'amount': 25},
        'gold_coins': {'chance': 0.2, 'graphics': 'graphics/items/gold_coins.png', 'amount': 75},
        'xp_orb': {'chance': 0, 'graphics': 'graphics/items/xp_orb.png', 'amount': 0}
    }

    # enemy
    monster_data = {
        'squid': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
        'crab': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
        'wizzard': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'slash', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
        'skeleton': {'loots': {'xp_orb', 'gold_coin', 'gold_coins'}, 'health': 100, 'exp': 150, 'damage': 8, 'attack_type': 'fireball', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350}
    }

    projectile_data = {
        'void': {'frames': 'graphics/particles/void', 'speed': 10, 'damage': 40, },
    }

    # weapons
    weapon_data = {
        'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'graphics/weapons/sword/up.png'},
        'lance': {'cooldown': 400, 'damage': 30, 'graphic': 'graphics/weapons/lance/up.png'},
        'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'graphics/weapons/axe/up.png'},
        'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'graphics/weapons/sai/up.png'}}

    ENERGY_CONSUMPTION_PER_FRAME = 0.35
    ENERGY_REGENERATION_PER_INTERVAL = 4
    ENERGY_REGENERATION_INTERVAL = 1000

    # MENU UI
    MENU_BORDER_COLOR = '#551C03'
    MENU_BG_COLOR = '#F9AA5E'
    MENU_BUTTON_BG_COLOR = '#EE7F26'

    INVENTORY_BG_COLOR = '#F9AA5E'
    INVENTORY_BORDER_COLOR = '#551C03'
    INVENTORY_SELECTED_BG_COLOR = '#c56307'

    GREEN_TEXT_COLOR = '#00FF00'
    RED_TEXT_COLOR = '#FF0000'

    # UI
    BAR_HEIGHT = 20
    HEALTH_BAR_WIDTH = 200
    ENERGY_BAR_WIDTH = 140
    ITEM_BOX_SIZE = 80
    UI_FONT = 'graphics/font/joystix.ttf'
    UI_FONT_SIZE = 18

    # general colors
    WATER_COLOR = '#71ddee'
    UI_BG_COLOR = '#222222'
    UI_BORDER_COLOR = '#111111'
    TEXT_COLOR = '#EEEEEE'

    # UI colors
    HEALTH_COLOR = 'red'
    ENERGY_COLOR = '#013220'

    # talent menu
    BLACK_TEXT_COLOR = '#111111'
    WHITE_TEXT_COLOR = '#EEEEEE'
    BAR_COLOR = '#EEEEEE'
    BAR_COLOR_SELECTED = '#111111'
    TALENT_BG_COLOR_SELECTED = '#EEEEEE'

    DAMAGE_NUMBER_COLOR = '#ff7200'

    npc_data = {
        '59': {'name': 'Laci 59', 'skin': 'Villager1', 'quest_ids': [4, 6], 'type': 'quest_giver', 'item_list': None},
        '79': {'name': 'Roli 79', 'skin': 'Villager1', 'quest_ids': [5], 'type': 'quest_giver', 'item_list': None},
        '119': {'name': 'Matyi 119', 'skin': 'Villager1', 'type': 'merchant', 'item_list': [0, 1, 2]},
        '99': {'name': 'Kevin 99', 'skin': 'Villager1', 'type': 'quest_giver', 'quest_ids': [3, 7], 'item_list': None},
        '139': {'name': 'Mate 139 ', 'skin': 'Villager1', 'quest_ids': [1, 2], 'type': 'quest_giver', 'item_list': None}
    }

    quest_data = {
        0: {
            'text': 'Open the control panel',
            'objective': 'Press f1 to open the controls panel',
            'max_amount': 1,
            'quest_type': 'open_control_panel',
            'rewardMoney': 400,
            'rewardXP': 300
        },
        1: {
            'text': 'Create a save',
            'objective': 'Save the game',
            'max_amount': 1,
            'quest_type': 'save_game',
            'rewardMoney': 400,
            'rewardXP': 400
        },
        2: {
            'text': 'Cut some grass',
            'objective': 'Grass cut',
            'max_amount': 50,
            'quest_type': 'cut_grass',
            'rewardMoney': 600,
            'rewardXP': 400
        },
        3: {
            'text': 'Go near the dungeon entrance and kill 3 skeletons',
            'objective': 'Kill 3 skeletons',
            'max_amount': 3,
            'quest_type': 'skeleton',
            'rewardMoney': 800,
            'rewardXP': 300
        },
        4: {
            'text': 'Buy some potions from the merchant',
            'objective': 'Buy potions',
            'max_amount': 3,
            'quest_type': 'buy_potion',
            'rewardMoney': 1000,
            'rewardXP': 500
        },
        5: {
            'text': 'Use a heal potion',
            'objective': 'Use a heal potion',
            'max_amount': 1,
            'quest_type': 'use_potion',
            'rewardMoney': 400,
            'rewardXP': 250
        },
        6: {
            'text': 'Kill the Crab in front of the dungeon entrance',
            'objective': 'Kill the Crab',
            'max_amount': 1,
            'quest_type': 'crab',
            'rewardMoney': 1500,
            'rewardXP': 600
        },
        7: {
            'text': 'Go into the dungeon and kill the Wizard',
            'objective': 'Kill the Wizard',
            'max_amount': 1,
            'quest_type': 'wizzard',
            'rewardMoney': 1500,
            'rewardXP': 800
        }
    }

    items = {

        0: {
            'id': 0,
            'name': 'Health Potion',
            'description': '',
            'type': 'consumable',
            'effect': 'health',
            'amount': 60,
            'duration': 0,
            'graphic': 'graphics/items/health_potion.png',
            'cost': 1000
        },
        1: {
            'id': 1,
            'name': 'Energy Potion',
            'description': '',
            'type': 'consumable',
            'effect': 'energy',
            'amount': 30,
            'duration': 0,
            'graphic': 'graphics/items/energy_potion.png',
            'cost': 1600
        },
        2: {
            'id': 2,
            'name': 'Strength Potion',
            'description': '',
            'type': 'consumable',
            'effect': 'strength',
            'amount': 10,
            'duration': 60,
            'graphic': 'graphics/items/strength_potion.png',
            'cost': 2000
        }
    }
