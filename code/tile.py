import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, settings, surface):
        super().__init__(groups)

        self.x = pos[0]
        self.y = pos[1]

        self.sprite_type = sprite_type
        y_offset = settings.HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(
                topleft=(self.x, self.y - settings.TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)
