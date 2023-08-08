import game_api_client
import json


class User():
    def __init__(self, username, user_id):
        self.username = username
        self.id = user_id
        self.characters = self.load_characters()

    def load_characters(self):
        characters = []
        for character_data in game_api_client.get_characters(self.id):
            # Create a Character object from the character data
            character = Character(character_data)
            characters.append(character)
        return characters


class Character():
    def __init__(self, character_data):
        self.player_name = character_data.get('player_name', 'Unknown')
        self.skin_id = character_data.get('skin_id', 0)
        self.x = character_data.get('x', 0)
        self.y = character_data.get('y', 0)
        self.stat_health = character_data.get('stat_health', 0)
        self.stat_energy = character_data.get('stat_energy', 0)
        self.stat_attack = character_data.get('stat_attack', 0)
        self.stat_speed = character_data.get('stat_speed', 0)
        self.health = character_data.get('health', 0)
        self.energy = character_data.get('energy', 0)
        self.xp = character_data.get('xp', 0)
        self.balance = character_data.get('balance', 0)

        self.player_completed_quests = [int(item_id) for item_id in json.loads(
            character_data.get('player_completed_quests', '[]'))]
        self.player_current_quest = character_data.get(
            'player_current_quest', -1)
        self.player_current_amount = character_data.get(
            'player_current_amount', 0)
        self.player_max_amount = character_data.get('player_max_amount', 1)
        self.player_inventory_item_ids = [int(item_id) for item_id in json.loads(
            character_data.get('player_inventory_item_ids', '[]'))]

        self.difficulty = character_data.get('difficulty', 1)
        self.level = character_data.get('level', 0)
        self.uid = character_data.get('uid', None)
        self.id = character_data.get('id', None)

    def generate_character_json(self):
        character_json = {
            "player_name": self.player_name,
            "skin_id": self.skin_id,
            "player_pos": [self.x, self.y],
            "player_stats": {
                "health": self.stat_health,
                "energy": self.stat_energy,
                "attack": self.stat_attack,
                "speed": self.stat_speed
            },
            "player_health": self.health,
            "player_energy": self.energy,
            "player_exp": self.xp,
            "balance": self.balance,
            "player_completed_quests": self.player_completed_quests,
            "player_current_quest": self.player_current_quest,
            "player_current_amount": self.player_current_amount,
            "player_max_amount": self.player_max_amount,
            "player_inventory_item_ids": self.player_inventory_item_ids,
            "difficulty": self.difficulty,
            "level": self.level,
            "id": self.id
        }
        return character_json
