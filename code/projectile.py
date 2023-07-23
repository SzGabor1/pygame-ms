import pygame
from support import import_folder
import math


class Projectile(pygame.sprite.Sprite):
    def __init__(self,  groups, settings, begin_pos, end_pos, projectile_type):
        super().__init__(groups)
        self.sprite_type = 'projectile'
        self.settings = settings
        self.projectile_type = projectile_type
        self.frames = import_folder(
            self.settings.projectile_data[self.projectile_type]['frames'])

        self.animation_start_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.begin_pos = begin_pos
        self.end_pos = end_pos
        self.animation_time = 4000
        self.image = pygame.transform.scale(
            self.frames[self.frame_index], (40, 40))
        self.rect = self.image.get_rect(center=begin_pos)

    def animate(self):
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.frame_index += 1

    def move_projectile(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.animation_start_time
        progress = elapsed_time / self.animation_time * \
            self.settings.projectile_data[self.projectile_type]['speed']

        if progress >= 1.0:
            self.rect.x = self.end_pos[0]
            self.rect.y = self.end_pos[1]
        else:
            direction_vector = (
                self.end_pos[0] - self.begin_pos[0], self.end_pos[1] - self.begin_pos[1])
            magnitude = math.sqrt(
                direction_vector[0]**2 + direction_vector[1]**2)
            normalized_direction = (
                direction_vector[0] / magnitude, direction_vector[1] / magnitude)
            distance = magnitude * progress

            self.rect.x = self.begin_pos[0] + \
                normalized_direction[0] * distance
            self.rect.y = self.begin_pos[1] + \
                normalized_direction[1] * distance

    def kill_projectile(self, player):
        if self.rect.colliderect(player.rect):
            self.kill()
            player.get_damage(
                self.settings.projectile_data[self.projectile_type]['damage'])
        elif math.sqrt((self.rect.x - self.end_pos[0]) ** 2 + (self.rect.y - self.end_pos[1]) ** 2) <= 10:
            self.kill()

    def update(self):
        self.animate()
        self.move_projectile()

    def update_projectile(self, player):
        self.kill_projectile(player)
