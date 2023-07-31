from typing import Any
import pygame
from npc import NPC
from shop import Shop


class Merchant(NPC):
    def __init__(self, npc_name, pos, groups, obstacle_sprites, id, item_list):
        super().__init__(npc_name, pos, groups, obstacle_sprites, id)

        self.itemlist = item_list

        self.toggle_shop = False

        self.shop = Shop(self.itemlist,
                         self.update_toggle_shop, self.name)

    def show_shop_button(self, player):
        if self.range_of_player and not self.toggle_shop:
            self.shop.display_shop_button()

    def show_shop(self, player):
        if self.range_of_player and self.toggle_shop:
            self.shop.display(player, pygame.event.get())
            self.shop.update()

    def update(self):
        self.input()

    def update_toggle_shop(self):
        self.toggle_shop = not self.toggle_shop

    def npc_update(self, player):
        self.in_range_of_player(player)
        self.show_shop(player)
        self.show_shop_button(player)
