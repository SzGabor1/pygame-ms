import pygame
from tile import Tile
from support import import_folder_sorted, import_csv_layout
from settings import Settings


class Animation():
    def __init__(self, ):
        super().__init__()
        self.animation_index = 0
        self.animation_time = None
        self.can_get_new_animation_frame = True
        self.animation_cooldown_time = 500
        self.animation_frames = []
        self.animation_tiles = []

        self.animation_layout = import_csv_layout(
            'new_map/MSmap._animated.csv')

        self.load_animation_frames()

    def load_animation_frames(self):
        for tile_id, image_path in Settings.map_animation_data.items():
            images = []
            images = import_folder_sorted(image_path)
            self.animation_frames.append((tile_id, images))

    def animate_map(self, visible_sprites, obstacle_sprites):
        if self.can_get_new_animation_frame:
            if self.animation_index >= len(self.animation_frames[0][1]):
                self.animation_index = 0

            for tile in self.animation_tiles:
                tile.kill()  # Remove all old animated tiles

            for row_index, row in enumerate(self.animation_layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * Settings.TILESIZE
                        y = row_index * Settings.TILESIZE

                        for tile_id, animation_frame in self.animation_frames:
                            if col == tile_id:
                                self.animation_tiles.append(Tile((x, y + 64), [visible_sprites,
                                                                               obstacle_sprites], 'object',  animation_frame[self.animation_index]))

            self.animation_time = pygame.time.get_ticks()
            self.can_get_new_animation_frame = False

    def animation_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_get_new_animation_frame:
            if current_time - self.animation_time >= self.animation_cooldown_time:
                self.animation_index += 1
                self.can_get_new_animation_frame = True

    def update(self, visible_sprites, obstacle_sprites):
        self.animate_map(visible_sprites, obstacle_sprites)
        self.animation_cooldown()
