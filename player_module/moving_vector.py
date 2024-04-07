from const import *
from geometry_abstractions import Vector


class PlayerMovingVector(Vector):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        self.key_right = False
        self.key_left = False
        self.key_up = False
        self.key_down = False

    def keydown(self, key) -> None:
        if key == LEFT:
            self.key_left = True
        elif key == RIGHT:
            self.key_right = True
        elif key == UP:
            self.key_up = True
        elif key == DOWN:
            self.key_down = True

    def keyup(self, key) -> None:
        if key == LEFT:
            self.key_left = False
        elif key == RIGHT:
            self.key_right = False
        elif key == UP:
            self.key_up = False
        elif key == DOWN:
            self.key_down = False

    def update(self) -> None:
        if self.key_right == self.key_left:
            self.x = 0
        elif self.key_right and not self.key_left:
            self.x = SPEED
        elif self.key_left and not self.key_right:
            self.x = -SPEED

        if self.key_up == self.key_down:
            self.y = 0
        elif self.key_up and not self.key_down:
            self.y = -SPEED
        elif self.key_down and not self.key_up:
            self.y = SPEED
