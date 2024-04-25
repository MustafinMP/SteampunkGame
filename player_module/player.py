import pygame
from pygame.sprite import Sprite, Group, collide_rect, spritecollideany
import load_data
from const import WIDTH, HEIGHT, Colors, Key
from player_module.moving_vector import PlayerMovingVector
from player_module.player_image_controller import PlayerImageController


class PlayerData:  # переместить в другое место, отвязать от сцены и спрайта игрока, привязать к классу игры
    def __init__(self):
        self.hp = 10
        self.max_hp = 10

        self.inventory = Inventory()


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

        self.data = PlayerData()

    def __init_shadow(self, *group) -> None:
        self.shadow = Sprite(*group)
        self.shadow.image = load_data.load_image('shadow.png')
        self.shadow.rect = self.shadow.image.get_rect()
        self.__update_shadow_coord()

    def __collide_doors(self, doors_group: Group) -> bool:
        return any([not door.is_opened and collide_rect(self, door) for door in doors_group])

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

    def draw_hp(self, screen) -> None:
        # не отображаем шкалу здоровья, если оно полное
        if self.data.hp == self.data.max_hp:
            return None
        pygame.draw.rect(screen, Colors.grey,
                         (self.rect.x, self.rect.y - 16, self.rect.width, 4),
                         0)
        pygame.draw.rect(screen, Colors.red,
                         (self.rect.x, self.rect.y - 16, self.rect.width * self.data.hp // self.data.max_hp, 4),
                         0)

    def keydown(self, key: Key) -> None:
        self.mv.keydown(key)

    def keyup(self, key: Key) -> None:
        self.mv.keyup(key)


class Inventory:  # переместить в отдельный файл
    def __init__(self):
        self.inventory = dict()

    def __getitem__(self, item):
        return self.inventory[item]

    def add(self, item, count=1) -> None:
        if item in self.inventory.keys():
            self.inventory[item] += count
        else:
            self.inventory[item] = count

    def count(self, item) -> int:
        if item in self.inventory.keys():
            return self.inventory[item]

    def get(self, item, count) -> int:
        if item in self.inventory.keys():
            real_count = self.inventory[item]
            if real_count < count:
                self.inventory[item] = 0
                return real_count
            self.inventory[item] -= count
            return count
        raise KeyError
