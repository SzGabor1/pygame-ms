import os
import json


class Save:
    def __init__(self):
        pass

    def update(self, player):
        self.player_name = player.name
        self.character_id = player.character_id
        self.player_pos = (player.hitbox.x, player.hitbox.y)
        self.player_stats = player.stats
        self.player_exp = player.exp
        self.player_balance = player.balance
        self.player_completed_quests = player.completed_quests
        self.player_current_quest = player.current_quest
        self.player_current_amount = player.current_amount
        self.player_max_amount = player.max_amount
        self.player_inventory_item_ids = player.inventory.get_items()


def create_save(player_name, character_id):
    player_pos = None
    player_stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed': 6}
    player_exp = 0
    player_balance = 0
    player_completed_quests = []
    player_current_quest = -1
    player_current_amount = 0
    player_max_amount = 1
    player_inventory_item_ids = []

    save_data = {
        'player_name': player_name,
        'character_id': character_id,
        'player_pos': player_pos,
        'player_stats': player_stats,
        'player_exp': player_exp,
        'player_balance': player_balance,
        'player_completed_quests': player_completed_quests,
        'player_current_quest': player_current_quest,
        'player_current_amount': player_current_amount,
        'player_max_amount': player_max_amount,
        'player_inventory_item_ids': player_inventory_item_ids
    }

    save_path = os.path.join(os.getcwd(), 'saves', player_name + '.json')

    with open(save_path, 'w') as file:
        json.dump(save_data, file)

    print(f"Save created: {save_path}")


def get_save_files(path, format):
    if format == "files":
        save_files = []
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if file_name.endswith(".json"):
                    save_files.append(file_name)
        return save_files
    else:
        save_files = []
        if os.path.exists(path):
            for file_name in os.listdir(path):
                if file_name.endswith(".json"):
                    file_path = os.path.join(path, file_name)
                    file_modified_time = os.path.getmtime(file_path)
                    save_files.append((file_name[:-5], file_modified_time))
        # Rendezés módosítási idő alapján
        save_files.sort(key=lambda x: x[1], reverse=True)
        return [file_name for file_name, _ in save_files]
