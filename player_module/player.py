from pygame.sprite import Sprite, Group, spritecollideany
import load_data
from const import WIDTH, HEIGHT, Key
from player_module.moving_vector import PlayerMovingVector
from player_module.player_image_controller import PlayerImageController


class PlayerSprite(Sprite):
    def __init__(self, scene, game_position: list[int, int] | tuple[int, int], *group) -> None:
        super().__init__(*group)
        self.scene = scene
        self.images = PlayerImageController()
        self.image = self.images.main_image

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.game_position: list = game_position
        self.mv = PlayerMovingVector()

        self.shadow = None
        self.__init_shadow(*group)

    def __init_shadow(self, *group) -> None:
        self.shadow = Sprite(*group)
        self.shadow.image = load_data.load_image('shadow.png')
        self.shadow.rect = self.shadow.image.get_rect()
        self.__update_shadow_coord()

    def __move(self, barriers: Group) -> None:
        """Меняем позицию игрока, если это возможно"""
        self.shadow.rect.x += self.mv.x
        if not spritecollideany(self.shadow, barriers):
            self.game_position[0] += self.mv.x
        self.shadow.rect.x -= self.mv.x

        self.shadow.rect.y += self.mv.y
        if not spritecollideany(self.shadow, barriers):
            self.game_position[1] += self.mv.y
        self.shadow.rect.y -= self.mv.y

    def __update_image(self):
        if self.mv.x == 0 and self.mv.y == 0:
            image = self.images.update_image(self.images.STAY)
        else:
            image = self.images.update_image(self.images.RUNNING, self.mv.x, self.mv.y)
        self.image = image

    def __update_shadow_coord(self) -> None:
        self.shadow.rect.x = self.rect.x
        self.shadow.rect.y = self.rect.y + self.rect.height // 3 * 2

    def update(self, barriers: Group) -> None:
        self.__update_shadow_coord()
        self.mv.update()
        self.__move(barriers)
        self.__update_image()

    def set_position(self, game_position: list[int, int] | tuple[int, int]) -> None:
        self.game_position: list = game_position

    def keydown(self, key: Key) -> None:
        self.mv.keydown(key)

    def keyup(self, key: Key) -> None:
        self.mv.keyup(key)
