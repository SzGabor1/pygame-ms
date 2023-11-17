import pygame
import time
from sound import Sounds
from settings import Settings


class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item_id):
        # Ellenőrizzük, hogy az item id már szerepel-e a listában
        for item in self.items:
            if item[0] == item_id:
                # Ha igen, növeljük a mennyiséget 1-gyel
                item[1] += 1
                return
        # Ha nem szerepel, hozzáadjuk az itemet a listához
        self.items.append([item_id, 1])

    def get_items(self):
        return self.items

    def remove_item(self, item_id):
        # Ellenőrizzük, hogy az item id szerepel-e a listában
        for item in self.items:
            if item[0] == item_id:
                # Csökkentjük a mennyiséget 1-gyel, és ha nulla vagy annál kisebb, eltávolítjuk az itemet
                item[1] -= 1
                if item[1] <= 0:
                    self.items.remove(item)
                return

    def display_items(self, ):
        for item_id, quantity in self.items:
            item_data = Settings.items[item_id]
            print(item_data['name'])

    def display_item(self, inventory_index):
        try:
            item_id, quantity = self.items[inventory_index]
            item_data = Settings.items[item_id]
            print(item_data['name'])
        except IndexError:
            pass

    def use_item(self, inventory_index, player):
        try:
            item_id, quantity = self.items[inventory_index]
            item_data = Settings.items[item_id]

            if item_data['type'] == 'consumable':
                print("Used: " + item_data['name'])
                self.use_consumable(item_data, player)
                self.remove_item(item_id)

        except IndexError:
            print('Invalid inventory index')

    def use_consumable(self, item_data, player):
        effect = item_data['effect']

        if effect == 'health':
            print("Used: " + item_data['name'])
            if (player.health + item_data['amount']) > player.stats[effect]:
                player.health = player.stats[effect]
                player.progress_quest('use_potion')

            else:
                player.health += item_data['amount']
        elif effect == 'energy':
            print("Used: " + item_data['name'])
            if (player.energy + item_data['amount']) > player.stats[effect]:
                player.energy = player.stats[effect]
            else:
                player.energy += item_data['amount']
        elif effect == 'strength':
            print("Used: " + item_data['name'])
            player.use_strength_potion()
