import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, settings, surface):
        super().__init__(groups)

        self.sprite_type = sprite_type
        y_offset = settings.HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object':
            self.rect = self.image.get_rect(
                topleft=(pos[0], pos[1] - settings.TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)
