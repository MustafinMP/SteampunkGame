from const import STEP


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
        obj.rect.x = obj.game_position.x + self.dx
        obj.rect.y = obj.game_position.y + self.dy

    def update(self, target):
        self.target = target
        w, h = self.screen_size
        self.target.rect.x = w // 2 - self.target.rect.width // 2
        self.target.rect.y = h // 2 - self.target.rect.height // 2
        try:
            self.dx = -(target.game_position.x - target.rect.x)
            self.dy = -(target.game_position.y - target.rect.y - target.rect.height + STEP)
        except AttributeError:
            print(type(target.game_position), target.game_position, type(target))

    def update_screen_size(self, new_screen_size: (int, int)):
        self.screen_size = new_screen_size
        self.update(self.target)