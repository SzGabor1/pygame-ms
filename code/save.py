import os
import json
import game_api_client


class Save:
    def __init__(self, save_parameters, characters):
        self.save_parameters = save_parameters
        self.characters = characters

    def load_data(self):
        if self.save_parameters[0] == 'existing':
            full_path = os.path.join(os.getcwd(), 'saves',
                                     self.save_parameters[1] + '.json')
            print(json.load(open(full_path)))
            return "existing", json.load(open(full_path))
        elif self.save_parameters[0] == 'online':
            return "online", self.load_online_save()
        elif self.save_parameters[0] == 'new':
            return "new", {'player_name': self.save_parameters[1], 'skin_id': self.save_parameters[2], 'difficulty': self.save_parameters[3]}
        elif self.save_parameters[0] == 'new_online':
            return "new", {'player_name': self.save_parameters[1], 'skin_id': self.save_parameters[2], 'difficulty': self.save_parameters[3], 'is_online': True, 'uid': self.save_parameters[4]}

    def load_online_save(self):
        for character in self.characters:
            if character.player_name == self.save_parameters[1]:
                return character.generate_character_json()

    def create_save(self, player):
        print("player name" + player.name)
        player_name = player.name
        skin_id = player.character_id
        player_pos = player.rect.topleft
        player_stats = player.stats
        player_health = player.health
        player_energy = player.energy
        player_exp = player.exp
        balance = player.balance
        player_completed_quests = player.completed_quests
        player_current_quest = player.current_quest
        player_current_amount = player.current_amount
        player_max_amount = player.max_amount
        player_inventory_item_ids = player.inventory.get_items()
        difficulty = player.difficulty

        save_data = {
            'player_name': player_name,
            'skin_id': skin_id,
            'player_pos': player_pos,
            'player_stats': player_stats,
            'player_health': player_health,
            'player_energy': player_energy,
            'player_exp': player_exp,
            'balance': balance,
            'player_completed_quests': player_completed_quests,
            'player_current_quest': player_current_quest,
            'player_current_amount': player_current_amount,
            'player_max_amount': player_max_amount,
            'player_inventory_item_ids': player_inventory_item_ids,
            'difficulty': difficulty,

        }

        save_path = os.path.join(os.getcwd(), 'saves',
                                 self.save_parameters[1] + '.json')

        with open(save_path, 'w') as file:
            json.dump(save_data, file)

        print(f"Save created: {save_path}")

    def create_new_online_save(self, player, user_id, level):

        print("new online player name " + player.name)
        player_name = player.name
        skin_id = player.character_id
        player_pos = player.rect.topleft
        player_stats = player.stats
        player_health = int(player.health)
        player_energy = int(player.energy)
        player_exp = player.exp
        balance = player.balance
        player_completed_quests = player.completed_quests
        player_current_quest = player.current_quest
        player_current_amount = player.current_amount
        player_max_amount = player.max_amount
        player_inventory_item_ids = player.inventory.get_items()
        difficulty = player.difficulty
        level = level

        save_data = {
            'player_name': player_name,
            'skin_id': skin_id,
            'x': player_pos[0],
            'y': player_pos[1],
            'stat_health': player_stats['health'],
            'stat_energy': player_stats['energy'],
            'stat_attack': player_stats['attack'],
            'stat_speed': player_stats['speed'],
            'health': player_health,
            'energy': player_energy,
            'xp': player_exp,
            'balance': balance,
            'player_completed_quests': str(player_completed_quests),
            'player_current_quest': player_current_quest,
            'player_current_amount': player_current_amount,
            'player_max_amount': player_max_amount,
            'player_inventory_item_ids': str(player_inventory_item_ids),
            'difficulty': difficulty,
            'level': level,
            "id": 0,  # placeholder only
            'uid': user_id,
        }

        print(game_api_client.create_character(save_data))

    def create_online_save(self, player, character_id, user_id, level):

        print("player name" + player.name)
        player_name = player.name
        skin_id = player.character_id
        player_pos = player.rect.topleft
        player_stats = player.stats
        player_health = int(player.health)
        player_energy = int(player.energy)
        player_exp = player.exp
        balance = player.balance
        player_completed_quests = player.completed_quests
        player_current_quest = player.current_quest
        player_current_amount = player.current_amount
        player_max_amount = player.max_amount
        player_inventory_item_ids = player.inventory.get_items()
        difficulty = player.difficulty

        save_data = {
            'player_name': player_name,
            'skin_id': skin_id,
            'x': player_pos[0],
            'y': player_pos[1],
            'stat_health': player_stats['health'],
            'stat_energy': player_stats['energy'],
            'stat_attack': player_stats['attack'],
            'stat_speed': player_stats['speed'],
            'health': player_health,
            'energy': player_energy,
            'xp': player_exp,
            'balance': balance,
            'player_completed_quests': str(player_completed_quests),
            'player_current_quest': player_current_quest,
            'player_current_amount': player_current_amount,
            'player_max_amount': player_max_amount,
            'player_inventory_item_ids': str(player_inventory_item_ids),
            'difficulty': difficulty,
            'level': level,
            'uid': user_id,
            'id': character_id
        }

        print(game_api_client.update_character(
            character_id, save_data))


def get_save_files(path):

    save_files = []
    if os.path.exists(path):
        for file_name in os.listdir(path):
            if file_name.endswith(".json"):
                file_path = os.path.join(path, file_name)
                file_modified_time = os.path.getmtime(file_path)
                save_files.append((file_name[:-5], file_modified_time))
    save_files.sort(key=lambda x: x[1], reverse=True)
    return [file_name for file_name, _ in save_files]
