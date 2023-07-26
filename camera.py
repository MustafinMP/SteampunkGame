from const import STEP, X, Y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.position[X] + self.dx
        obj.rect.y = obj.position[Y] + self.dy

    def update(self, target):
        self.dx = -(target.position[X] - target.rect.x)
        self.dy = -(target.position[Y] - target.rect.y - target.rect.height + STEP)