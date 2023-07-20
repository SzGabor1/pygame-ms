import pygame
from support import import_folder
from random import choice
import math


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # magic
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            'void': import_folder('graphics/particles/void'),

            # attacks
            'claw': import_folder('graphics/particles/claw'),
            'slash': import_folder('graphics/particles/slash'),
            'sparkle': import_folder('graphics/particles/sparkle'),
            'leaf_attack': import_folder('graphics/particles/leaf_attack'),
            'thunder': import_folder('graphics/particles/thunder'),

            # monster deaths
            'squid': import_folder('graphics/particles/smoke_orange'),
            'crab': import_folder('graphics/particles/crab'),
            'wizzard': import_folder('graphics/particles/nova'),
            'skeleton': import_folder('graphics/particles/nova'),
            'bamboo': import_folder('graphics/particles/bamboo'),

            # leafs
            'leaf': (
                import_folder('graphics/particles/leaf1'),
                import_folder('graphics/particles/leaf2'),
                import_folder('graphics/particles/leaf3'),
                import_folder('graphics/particles/leaf4'),
                import_folder('graphics/particles/leaf5'),
                import_folder('graphics/particles/leaf6'),
                self.reflect_images(import_folder(
                    'graphics/particles/leaf1')),
                self.reflect_images(import_folder(
                    'graphics/particles/leaf2')),
                self.reflect_images(import_folder(
                    'graphics/particles/leaf3')),
                self.reflect_images(import_folder(
                    'graphics/particles/leaf4')),
                self.reflect_images(import_folder(
                    'graphics/particles/leaf5')),
                self.reflect_images(import_folder(
                    'graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

    def create_projectile_particles(self, projectile_type, begin_pos, pos, groups):
        animation_frames = self.frames[projectile_type]
        TimeBasedParticleEffect(begin_pos, pos, animation_frames, groups)


class TimeBasedParticleEffect(pygame.sprite.Sprite):

    def __init__(self, begin_pos, pos, animation_frames, groups):
        super().__init__(groups)
        self.animation_start_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.begin_pos = begin_pos
        self.end_pos = pos  # Add end_pos to store the final position
        self.animation_time = 4000
        self.frames = animation_frames
        self.image = pygame.transform.scale(
            self.frames[self.frame_index], (40, 40))
        self.rect = self.image.get_rect(center=begin_pos)

    def animate(self):
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.frame_index += 1

    def move_projectile(self):
        direction_vector = (
            self.end_pos[0] - self.begin_pos[0], self.end_pos[1] - self.begin_pos[1])
        magnitude = math.sqrt(direction_vector[0]**2 + direction_vector[1]**2)
        normalized_direction = (
            direction_vector[0] / magnitude, direction_vector[1] / magnitude)
        speed = 10
        self.rect.x += normalized_direction[0] * speed
        self.rect.y += normalized_direction[1] * speed

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_start_time >= self.animation_time:
            self.kill()

    def update(self):
        self.animate()
        self.cooldown()
        self.move_projectile()


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
