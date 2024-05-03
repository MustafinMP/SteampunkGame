import pygame
import json
import sys
import os


def load_image(filename: str, colorkey=None):
    """Загрузка изображений для спрайтов"""
    fullname = os.path.join('data/sprites', filename)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_game_container(filename: str) -> dict:
    file = open(filename)
    container = json.load(file)
    file.close()
    return container