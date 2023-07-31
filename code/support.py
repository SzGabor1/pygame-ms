from csv import reader
import os
from os import walk
import pygame
import re
import json


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_sorted(path):
    surface_list = []

    # Get all the file paths in the directory and sort them in numeric order
    def sort_key(filename):
        return int(re.search(r'\d+', filename).group())

    file_paths = [os.path.join(path, f) for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]
    file_paths.sort(key=sort_key)

    for full_path in file_paths:
      #  print(full_path)
        image_surf = pygame.image.load(full_path).convert_alpha()
        surface_list.append(image_surf)

    return surface_list


def import_settings(path):
    f = open(path)

    # returns JSON object as a dictionary
    data = json.load(f)

    f.close()
    return data

    # Closing file


def import_character_profile_images():
    from settings import Settings
    character_images = []
    for character_id in Settings.character_ids:
        image_path = os.path.join(
            "graphics", "characters", "players", character_id, "profile", "profile.png")
        image = pygame.image.load(image_path).convert_alpha()
        character_images.append(image)
    return character_images
