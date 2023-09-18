import pygame
from settings import Settings


class Loot(pygame.sprite.Sprite):
    def __init__(self, groups, pos, itemname):
        super().__init__(groups)
        self.x = pos[0]
        self.y = pos[1]
        self.sprite_type = 'loot'
        self.itemname = itemname
        self.amount = Settings.loots.get(self.itemname, {}).get('amount', 1)
        graphics_path = Settings.loots.get(
            self.itemname, {}).get('graphics', None)

        if graphics_path is not None:
            self.image = pygame.image.load(graphics_path).convert_alpha()
        else:
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 0))
            print(
                f"No itemname defined: '{self.itemname}'")

        self.rect = self.image.get_rect(center=pos)
        self.item = None
