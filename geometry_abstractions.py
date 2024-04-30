from __future__ import annotations


class Vector:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: Vector) -> Vector:
        return self.__add__(other)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __isub__(self, other: Vector) -> Vector:
        return self.__sub__(other)


def scale(iter_obj: list[int, int] | tuple[int, int], ratio: int) -> list[int, int]:
    return [elem * ratio for elem in iter_obj]
