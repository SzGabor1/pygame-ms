# game setup

WIDTH = 1680
HEIGHT = 950
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'building': -40,
    'grass': -10,
    'invisible': 0
}

# weapons
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic': 'graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 300, 'graphic': 'graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphic': 'graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphic': 'graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphic': 'graphics/weapons/sai/full.png'}}

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
ENERGY_COLOR = 'blue'

# talent menu
BLACK_TEXT_COLOR = '#111111'
WHITE_TEXT_COLOR = '#EEEEEE'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
TALENT_BG_COLOR_SELECTED = '#EEEEEE'

# enemy
monster_data = {
    'squid': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'attack_sound': 'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300, 'exp': 250, 'damage': 40, 'attack_type': 'claw',  'attack_sound': 'audio/attack/claw.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100, 'exp': 110, 'damage': 8, 'attack_type': 'thunder', 'attack_sound': 'audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350}
}


npc_data = {
    '256': {'name': 'Villager256', 'quest_ids': [0]},
    '-2147483254': {'name': 'Villager-2147483254', 'quest_ids': [1]},
    '257': {'name': 'Villager257', 'quest_ids': [2]},
    '258': {'name': 'Villager258', 'quest_ids': []},
    '259': {'name': 'Villager259', 'quest_ids': []}
}

quest_data = {
    0: {
        "text": "Öld meg a szellemeket",
        "objective": "Ölj meg 3 szellemet",
        "max_amount": 3,
        "enemy_type": "spirit",
        "rewardMoney": 200,
        "rewardXP": 3010
    },

    1: {
        "text": "Öld meg a racoont",
        "objective": "Öld meg a racoont",
        "max_amount": 1,
        "enemy_type": "raccoon",
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
