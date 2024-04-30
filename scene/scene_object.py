from __future__ import annotations
from custom_sprite import CustomSprite
import load_data


class SceneObject:
    """Фасад. Инкапсулирует в себе спрайт игровго предмета или персонажа."""
    def __init__(self, scene, position, image, shadow_image=None) -> None:
        self.scene = scene
        self.main_sprite = SceneObjectSprite(scene, position, image)
        if shadow_image is None:
            shadow_image = image
        self.shadow_sprite = ShadowSprite(shadow_image)
        self.shadow_sprite.update_coord(self.main_sprite.rect)
        self.game_position = position

    def set_position(self, game_position: list[int, int] | tuple[int, int]) -> None:
        self.game_position = game_position

    def update(self, others: list[SceneObject] | tuple[SceneObject] = ()) -> None:
        self.shadow_sprite.update_coord(self.main_sprite.rect)

    def collide_shadow(self, other_object: SceneObject) -> bool:
        return self.shadow_sprite.is_collided_with(other_object.shadow_sprite)

    def sort_key(self) -> int:
        return self.shadow_sprite.rect.centery

    def draw(self, screen) -> None:
        self.main_sprite.draw(screen)
        self.shadow_sprite.draw(screen)


class SceneObjectSprite(CustomSprite):
    def __init__(self, scene, position: list[int, int] | tuple[int, int], image: str) -> None:
        super().__init__()
        self.scene = scene
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position


class ShadowSprite(CustomSprite):
    def __init__(self, shadow_image: str) -> None:
        super().__init__()
        self.image = load_data.load_image(shadow_image)
        self.rect = self.image.get_rect()

    def update_coord(self, parent_rect) -> None:
        self.rect.x = parent_rect.x
        self.rect.y = parent_rect.bottom - self.rect.height

    def move_x(self, dx: int) -> None:
        self.rect.x += dx

    def move_y(self, dy: int) -> None:
        self.rect.y += dy
