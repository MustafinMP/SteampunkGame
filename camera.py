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
            obj.main_sprite.rect.x = w // 2 - obj.main_sprite.rect.width // 2
            obj.main_sprite.rect.y = h // 2 - obj.main_sprite.rect.height // 2
            return
        obj.main_sprite.rect.x = obj.game_position[0] + self.dx
        obj.main_sprite.rect.y = obj.game_position[1] + self.dy

    def update(self, target):
        self.target = target
        w, h = self.screen_size
        self.target.main_sprite.rect.x = (w - self.target.main_sprite.rect.width) // 2
        self.target.main_sprite.rect.y = (h - self.target.main_sprite.rect.height) // 2
        self.dx = target.main_sprite.rect.x - target.game_position[0]
        self.dy = target.main_sprite.rect.y + target.main_sprite.rect.height - target.game_position[1] - RATIO

    def update_screen_size(self, new_screen_size: (int, int)):
        self.screen_size = new_screen_size
        self.update(self.target)
