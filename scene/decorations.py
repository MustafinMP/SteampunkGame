from custom_sprite import CustomSprite, SceneObject
import load_data


class AbstractDecoration(CustomSprite):
    def __init__(self, scene, position: list[int, int] | tuple[int, int], image: str):
        super().__init__()
        self.scene = scene
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.game_position: list = position
        self.rect.x, self.rect.y = position


class Floor(AbstractDecoration):
    """Объект пола, всегда на заднем плане"""


class ActionPlace(AbstractDecoration):
    """Место, где возможно какое-либо действие"""

    def __init__(self, scene, position: list[int, int] | tuple[int, int], image, hint_image):
        super().__init__(scene, position, image)

        self.hint_label = CustomSprite()
        self.hint_label.image = load_data.load_image(hint_image)
        self.hint_label.rect = self.hint_label.image.get_rect()

        self.action_func = lambda *args: ...
        self.action_args: list = []

    def set_action(self, func, *args):
        self.action_func = func
        self.action_args = args

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def call_action(self):
        self.action_func(*self.action_args)

    def draw(self, screen, draw_hint=False):
        super().draw(screen)
        if draw_hint:
            screen_size = self.scene.game.screen_size
            self.hint_label.rect.x = screen_size[0] // 2 - 96
            self.hint_label.rect.y = screen_size[1] - 150
            self.hint_label.draw(screen)
