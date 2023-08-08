import game_api_client


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
        self.player_completed_quests = character_data.get(
            'player_completed_quests', '[]')
        self.player_current_quest = character_data.get(
            'player_current_quest', -1)
        self.player_current_amount = character_data.get(
            'player_current_amount', 0)
        self.player_max_amount = character_data.get('player_max_amount', 1)
        self.player_inventory_item_ids = character_data.get(
            'player_inventory_item_ids', '[]')
        self.difficulty = character_data.get('difficulty', 1)
        self.level = character_data.get('level', 0)
        self.uid = character_data.get('uid', None)
