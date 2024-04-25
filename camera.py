from const import RATIO


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.target = None
        self.screen_size = [0, 0]

    def apply(self, obj) -> None:
        if obj is self.target:
            w, h = self.screen_size
            obj.rect.x = w // 2 - obj.rect.width // 2
            obj.rect.y = h // 2 - obj.rect.height // 2
            return
        obj.rect.x = obj.game_position[0] + self.dx
        obj.rect.y = obj.game_position[1] + self.dy

    def update(self, target):
        self.target = target
        w, h = self.screen_size
        self.target.rect.x = w // 2 - self.target.rect.width // 2
        self.target.rect.y = h // 2 - self.target.rect.height // 2
        self.dx = -(target.game_position[0] - target.rect.x)
        self.dy = -(target.game_position[1] - target.rect.y - target.rect.height + RATIO)

    def update_screen_size(self, new_screen_size: (int, int)):
        self.screen_size = new_screen_size
        self.update(self.target)