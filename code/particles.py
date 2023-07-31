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

    def display_damage_numbers(self, pos, groups, damage, settings):
        DamageNumber(pos, damage, groups, settings)


class DamageNumber(pygame.sprite.Sprite):

    def __init__(self, pos, damage, groups, settings):
        self.settings = settings
        self.font = pygame.font.Font(
            self.settings.UI_FONT, self.settings.UI_FONT_SIZE)
        super().__init__(groups)
        self.damage = str(damage)
        self.image = self.font.render(
            self.damage, True, self.settings.DAMAGE_NUMBER_COLOR)
        self.rect = self.image.get_rect(center=pos)
        self.duration = 1000  # 1 second in milliseconds
        self.speed = 0.01
        self.dy = -self.speed
        self.animation_offset = self.dy * self.duration
        self.start_time = pygame.time.get_ticks()

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.start_time + self.duration:
            self.kill()
        else:
            progress = (current_time - self.start_time) / self.duration
            self.rect.y += int(self.animation_offset * progress)

    def update(self):
        self.animate()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


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
