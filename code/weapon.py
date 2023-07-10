import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.sprite_type = 'weapon'
        self.direction = None  # Initialize the direction attribute

        # graphic
        self.image = self.load_weapon_image()
        self.rect = self.image.get_rect()  # Create the rect attribute

        # placement
        self.update_weapon_position()

    def load_weapon_image(self):
        direction = self.player.status.split('_')[0]
        full_path = f'graphics/weapons/{self.player.weapon}/{direction}.png'
        return pygame.image.load(full_path).convert_alpha()

    def update_weapon_position(self):
        direction = self.player.status.split('_')[0]

        # Update weapon position based on the player's direction
        if direction == 'left':
            self.rect.midright = self.player.rect.midleft + \
                pygame.math.Vector2(0, 16)
        elif direction == 'right':
            self.rect.midleft = self.player.rect.midright + \
                pygame.math.Vector2(0, 16)
        elif direction == 'down':
            self.rect.midtop = self.player.rect.midbottom + \
                pygame.math.Vector2(-10, 0)
        else:
            self.rect.midbottom = self.player.rect.midtop + \
                pygame.math.Vector2(-10, 0)

        # Check if the player's direction has changed
        if direction != self.direction:
            self.image = self.load_weapon_image()  # Load the new weapon image
            self.direction = direction  # Update the stored direction

    def update(self):
        self.update_weapon_position()
