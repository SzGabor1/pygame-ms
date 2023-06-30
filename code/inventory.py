import pygame
import time


class Inventory:
    def __init__(self, settings):
        # general setup
        self.settings = settings
        # id, name matrix
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def display_items(self):
        for item in self.items:
            print(self.settings.items[item]['name'])

    def display_item(self, inventory_index):
        try:
            item = self.items[inventory_index]
            print(self.settings.items[item]['name'])
        except IndexError:
            pass

    def use_item(self, inventory_index, player):
        try:
            item = self.items[inventory_index]
            item_data = self.settings.items[item]

            if item_data['type'] == 'consumable':
                print("Used: " + item_data['name'])
                self.use_consumable(item_data, player, item_data['effect'])
                self.remove_item(item)

        except IndexError:
            print('Invalid inventory index')

    def use_consumable(self, item_data, player, effect):
        if(effect == 'health'):
            self.settings.potion_sound.play()
            if (player.health + item_data['amount']) > player.stats[effect]:
                player.health = player.stats[effect]

            else:
                player.health += item_data['amount']
        elif(effect == 'energy'):
            if (player.energy + item_data['amount']) > player.stats[effect]:
                player.energy = player.stats[effect]
            else:
                player.energy += item_data['amount']
        elif(effect == 'strength'):
            player.use_strength_potion()
