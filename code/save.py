import os
import json


class Save:
    def __init__(self, save_parameters):
        self.save_parameters = save_parameters

    def load_data(self):
        if self.save_parameters[0] == 'existing':
            full_path = os.path.join(os.getcwd(), 'saves',
                                     self.save_parameters[1] + '.json')
            print(json.load(open(full_path)))
            return "existing", json.load(open(full_path))
        else:
            return "new", {'player_name': self.save_parameters[1], 'character_id': self.save_parameters[2]}

    def create_save(self, player):
        print("save class, create_save")
        print("player name" + player.name)

        player_name = player.name
        character_id = player.character_id
        player_pos = player.rect.topleft
        player_stats = player.stats
        player_health = player.health
        player_energy = player.energy
        player_speed = player.speed
        player_exp = player.exp
        player_balance = player.balance
        player_completed_quests = player.completed_quests
        player_current_quest = player.current_quest
        player_current_amount = player.current_amount
        player_max_amount = player.max_amount
        player_inventory_item_ids = player.inventory.get_items()

        save_data = {
            'player_name': player_name,
            'character_id': character_id,
            'player_pos': player_pos,
            'player_stats': player_stats,
            'player_health': player_health,
            'player_energy': player_energy,
            'player_speed': player_speed,
            'player_exp': player_exp,
            'player_balance': player_balance,
            'player_completed_quests': player_completed_quests,
            'player_current_quest': player_current_quest,
            'player_current_amount': player_current_amount,
            'player_max_amount': player_max_amount,
            'player_inventory_item_ids': player_inventory_item_ids

        }

        save_path = os.path.join(os.getcwd(), 'saves',
                                 self.save_parameters[1] + '.json')

        with open(save_path, 'w') as file:
            json.dump(save_data, file)

        print(f"Save created: {save_path}")


def get_save_files(path):

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
