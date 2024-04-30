from custom_sprite import CustomSprite
from scene.scene_object import ShadowSprite, SceneObject, SceneObjectSprite
import load_data
from const import WIDTH, HEIGHT, Key
from player_module.moving_vector import PlayerMovingVector
from player_module.player_image_controller import PlayerImageController


class PlayerShadowSprite(ShadowSprite):
    def move_x(self, dx: int) -> None:
        self.rect.x += dx

    def move_y(self, dy: int) -> None:
        self.rect.y += dy


class PlayerSprite(SceneObjectSprite):
    def __init__(self, scene) -> None:
        self.images = PlayerImageController()
        super().__init__(scene, [0, 0], 'shadow.png')
        self.image = self.images.main_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.game_position = [0, 0]

    def move_x(self, dx: int) -> None:
        self.game_position[0] += dx
        self.rect.x += dx

    def move_y(self, dy: int) -> None:
        self.game_position[1] += dy
        self.rect.y += dy

    def update_image(self, mv: PlayerMovingVector) -> None:
        if mv.x == 0 and mv.y == 0:
            image = self.images.update_image(self.images.STAY)
        else:
            image = self.images.update_image(self.images.RUNNING, mv.x, mv.y)
        self.image = image


class Player(SceneObject):
    """Фасад. Инкапсулирует в себе спрайт игрока, его тень (объект контроля движения), управление игроком."""
    def __init__(self, scene) -> None:
        super().__init__(scene, (0, 0), 'shadow.png')
        self.main_sprite = PlayerSprite(scene)
        self.shadow_sprite = PlayerShadowSprite()
        self.shadow_sprite.update_coord(self.main_sprite.rect)

        self.moving_vector = PlayerMovingVector()

    def update(self, others: list[SceneObject] | tuple[SceneObject] = ()) -> None:
        super().update(others)
        self.moving_vector.update()
        self.move(others)
        self.main_sprite.update_image(self.moving_vector)

    def move(self, other_objects: list[SceneObject]) -> None:
        dx = self.moving_vector.x
        self.shadow_sprite.move_x(dx)
        if not any([obj.collide_shadow(self) for obj in other_objects]):
            self.main_sprite.move_x(dx)
        self.shadow_sprite.move_x(-dx)

        dy = self.moving_vector.y
        self.shadow_sprite.move_y(dy)
        if not any([obj.collide_shadow(self) for obj in other_objects]):
            self.main_sprite.move_y(dy)
        self.shadow_sprite.move_y(-dy)

    def keydown(self, key: Key) -> None:
        self.moving_vector.keydown(key)

    def keyup(self, key: Key) -> None:
        self.moving_vector.keyup(key)
