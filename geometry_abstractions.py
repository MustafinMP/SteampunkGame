from __future__ import annotations


class Coord:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: Coord | Vector | Position):
        return Coord(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Coord | Vector | Position):
        return self.__add__(other)

    def __sub__(self, other: Coord | Vector | Position):
        return Coord(self.x + other.x, self.y + other.y)

    def __isub__(self, other: Coord | Vector | Position):
        return self.__sub__(other)


class Vector(Coord):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)


class Position(Coord):
    """Поведение аналогично Coord, однако Position обозначает формальную позицию на игровом поле, в то время как Coord -
    координаты на экране."""
    ...
