from typing import TypeAlias
from pygame.color import Color as Color

Key: TypeAlias = int

FPS = 60
ANIMATION_FPS = 10
SPEED = 6
RATIO = 3  # коэффициент увеличения пикселя
WIDTH = 1200
HEIGHT = 700


class Keys:
    RIGHT: Key = 0
    LEFT: Key = 1
    UP: Key = 2
    DOWN: Key = 3


class Colors:
    red = Color(180, 0, 0)
    grey = Color(100, 100, 100)
    background = Color(20, 20, 20)
