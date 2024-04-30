from .scene_object import SceneObject
from custom_sprite import CustomSprite
import load_data


class ActionObject(SceneObject):
    def __init__(self, scene, position: list[int, int] | tuple[int, int], image: str, hint_image: str) -> None:
        super().__init__(scene, position, image, image)
        self.hint_label = CustomSprite()
        self.hint_label.image = load_data.load_image(hint_image)
        self.hint_label.rect = self.hint_label.image.get_rect()

        self.action_func = lambda *args: ...
        self.action_args: list = []

    def set_action(self, func: object, *args) -> None:
        self.action_func = func
        self.action_args = args

    def call_action(self) -> None:
        self.action_func(*self.action_args)

    def draw(self, screen, draw_hint: bool = False) -> None:
        super().draw(screen)
        if draw_hint:
            screen_size = self.scene.game.screen_size
            self.hint_label.rect.x = screen_size[0] // 2 - self.hint_label.rect.width // 2
            self.hint_label.rect.y = screen_size[1] - 150
            self.hint_label.draw(screen)