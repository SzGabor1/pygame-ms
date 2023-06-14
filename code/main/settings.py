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
    'lance': {'cooldown': 400, 'damage': 30, 'graphic': 'graphics/weapons/lance/full.png'},
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

quests = [
    {
        "title": "The Lost Artifact",
        "description": "Retrieve the ancient artifact hidden deep within the jungle.",
        "reward": "Rare gemstone and 500 gold coins."
    },
    {
        "title": "Monster Hunter",
        "description": "Slay five ferocious beasts terrorizing the nearby village.",
        "reward": "Legendary sword and a suit of enchanted armor."
    },
    {
        "title": "The Mysterious Puzzle",
        "description": "Solve a series of cryptic riddles to unlock the hidden treasure.",
        "reward": "Chest filled with valuable relics and a map to a secret location."
    },
    {
        "title": "The Forbidden Temple",
        "description": "Brave the dangers of the forbidden temple to retrieve the sacred idol.",
        "reward": "Eternal blessings and eternal knowledge."
    },
    {
        "title": "The Cursed Manor",
        "description": "Investigate the haunted manor and lift the curse that plagues its inhabitants.",
        "reward": "Gratitude of the spirits and a powerful talisman."
    }
]
