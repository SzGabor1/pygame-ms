import pygame
import math


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.sprite_type = 'weapon'

        self.original_image = self.load_weapon_image()
        self.image = self.original_image

        # placement
        self.rect = self.image.get_rect()
        self.direction = self.player.status.split('_')[0]
        self.angle = 0  # Initialize the angle of rotation

        self.update_weapon_position()

    def load_weapon_image(self):
        direction = self.player.status.split('_')[0]
        full_path = f'graphics/weapons/{self.player.weapon}/{direction}.png'
        return pygame.image.load(full_path).convert_alpha()

    def update_weapon_position(self):
        direction = self.player.status.split('_')[0]

        # Check if the player's direction has changed
        if direction != self.direction:
            self.image = self.load_weapon_image()  # Load the new weapon image
            self.direction = direction  # Update the stored direction

        # Update the rotation angle based on a sinusoidal function
        angular_speed = 0.1  # Adjust this value to control the speed of rotation
        amplitude = 60  # Adjust this value to control the amplitude of rotation
        self.angle += angular_speed
        rotation = math.sin(self.angle) * amplitude

        if direction == 'left':
            self.update_left_attack(rotation, amplitude)
        elif direction == 'right':
            self.update_right_attack(rotation, amplitude)
        elif direction == 'up':
            self.update_top_attack(rotation, amplitude)
        elif direction == 'down':
            self.update_bottom_attack(rotation, amplitude)

    def update_left_attack(self, rotation, amplitude):
        # Rotate the weapon image around the player's position
        rotated_image = pygame.transform.rotate(self.original_image, rotation)
        self.rect = rotated_image.get_rect(
            center=self.player.rect.midleft)  # Change midleft to midtop
        self.image = rotated_image

        offset_x = -16
        self.rect.x += offset_x

        # Adjust the position of the image based on the current state of the sin function
        offset_y = math.sin(self.angle) * amplitude * 0.5
        self.rect.y += offset_y

    def update_right_attack(self, rotation, amplitude):
        # Rotate the weapon image around the player's position
        rotated_image = pygame.transform.rotate(self.original_image, rotation)
        self.rect = rotated_image.get_rect(center=self.player.rect.midright)
        self.image = rotated_image

        offset_x = 16
        self.rect.x += offset_x

        offset_y = math.sin(self.angle) * amplitude * 0.5
        self.rect.y -= offset_y

    def update_top_attack(self, rotation, amplitude):
        # Rotate the weapon image around the player's position
        rotated_image = pygame.transform.rotate(self.original_image, rotation)
        self.rect = rotated_image.get_rect(center=self.player.rect.midtop)
        self.image = rotated_image

        offset_y = -20
        self.rect.y += offset_y

        offset_x = -math.sin(self.angle) * amplitude * 0.5
        self.rect.x += offset_x

    def update_bottom_attack(self, rotation, amplitude):
        # Rotate the weapon image around the player's position
        rotated_image = pygame.transform.rotate(self.original_image, rotation)
        self.rect = rotated_image.get_rect(center=self.player.rect.midbottom)
        self.image = rotated_image

        offset_y = 20
        self.rect.y += offset_y

        offset_x = math.sin(self.angle) * amplitude * 0.5
        self.rect.x += offset_x

    def update(self):
        self.update_weapon_position()
