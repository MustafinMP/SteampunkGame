from const import STEP, X, Y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.game_position[X] + self.dx
        obj.rect.y = obj.game_position[Y] + self.dy

    def update(self, target):
        self.dx = -(target.game_position[X] - target.rect.x)
        self.dy = -(target.game_position[Y] - target.rect.y - target.rect.height + STEP)