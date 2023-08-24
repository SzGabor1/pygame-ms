import pygame
from settings import Settings


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(groups)

        self.x = pos[0]
        self.y = pos[1]

        self.sprite_type = sprite_type
        y_offset = Settings.HITBOX_OFFSET[sprite_type]
        self.image = surface
        # object somehow +64 pixels on y level need correction
        if sprite_type == 'object':
            self.rect = self.image.get_rect(
                topleft=(self.x, self.y - Settings.TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)
