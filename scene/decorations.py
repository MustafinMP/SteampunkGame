from pygame.sprite import Sprite, Group
import load_data


class AbstractDecoration(Sprite):
    def __init__(self, position: list[int, int] | tuple[int, int], image: str, *group):
        super().__init__(*group)
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.game_position: list = position
        self.rect.x, self.rect.y = position


class Floor(AbstractDecoration):
    """Объект пола, всегда на заднем плане"""


class Barrier(AbstractDecoration):
    """Объект препятствий, восприимчив к столкновениям"""


class ActionPlace(AbstractDecoration):
    """Место, где возможно какое-либо действие"""

    def __init__(self, position: list[int, int] | tuple[int, int], image, hint_image, *group):
        super().__init__(position, image, *group)

        self.hint_group = Group()
        self.hint_label = Sprite(self.hint_group)
        self.hint_label.image = load_data.load_image(hint_image)
        self.hint_label.rect = self.hint_label.image.get_rect()
        self.update_hint_coord()

        self.action_func = lambda: ...
        self.action_args: list = []

    def update_hint_coord(self):
        self.hint_label.rect.x = self.rect.center[0] - 16
        self.hint_label.rect.y = self.rect.center[1] + 32

    def set_action(self, func, *args):
        self.action_func = func
        self.action_args = args

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw_hint(self, screen):
        self.update_hint_coord()
        self.hint_group.draw(screen)

    def call_action(self):
        self.action_func(*self.action_args)
