import pygame
from pygame.sprite import Sprite, Group, collide_rect, spritecollideany
import load_data
from const import *
import color


class Player(Sprite):
    """Главный класс персонажа.
    Хранит все сведения об нем (позиция на поле, анимации, сценарные характеристики, такие как здоровье), и т.д."""

    def __init__(self, position: list, *group) -> None:
        super().__init__(*group)
        self.image = load_data.load_image('player_x3.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [WIDTH // 2 - self.rect.width // 2,
                                    HEIGHT // 2 - self.rect.height // 2]
        # положение на игровом поле
        self.position = position
        self.vector_x = 0
        self.vector_y = 0
        self.key_right = False
        self.key_left = False
        self.key_up = False
        self.key_down = False

        self.shadow = None
        self.__init_shadow(*group)

        self.inventory = Inventory()

        self.hp = 10
        self.max_hp = 10

    def __init_shadow(self, *group) -> None:
        self.shadow = Sprite(*group)
        self.shadow.image = load_data.load_image('shadow.png')
        self.shadow.rect = self.shadow.image.get_rect()
        self.__update_shadow_coord()

    def __collide_doors(self, doors_group: Group) -> bool:
        return any([not door.is_opened and collide_rect(self, door) for door in doors_group])

    def __move(self, barriers: Group, doors_group: Group) -> None:
        """Меняем позицию игрока, если это возможно"""
        self.shadow.rect.x += self.vector_x
        if not (spritecollideany(self.shadow, barriers) or self.__collide_doors(doors_group)):
            self.position[X] += self.vector_x
        self.shadow.rect.x -= self.vector_x

        self.shadow.rect.y += self.vector_y
        if not (spritecollideany(self.shadow, barriers) or self.__collide_doors(doors_group)):
            self.position[Y] += self.vector_y
        self.shadow.rect.y -= self.vector_y

    def __update_shadow_coord(self) -> None:
        self.shadow.rect.x = self.rect.x
        self.shadow.rect.y = self.rect.y + self.rect.height // 3 * 2

    def __update_vectors(self) -> None:
        """Направление движения игрока в пространстве"""
        # update X vector
        if self.key_right == self.key_left:
            self.vector_x = 0
        elif self.key_right and not self.key_left:
            self.vector_x = SPEED
        elif self.key_left and not self.key_right:
            self.vector_x = -SPEED
        # update Y vector
        if self.key_up == self.key_down:
            self.vector_y = 0
        elif self.key_up and not self.key_down:
            self.vector_y = -SPEED
        elif self.key_down and not self.key_up:
            self.vector_y = SPEED

    def passive_update(self, size, barriers, doors_group) -> None:
        w, h = size
        self.rect.x, self.rect.y = [w // 2 - self.rect.width // 2,
                                    h // 2 - self.rect.height // 2]
        self.__update_shadow_coord()
        self.__update_vectors()
        self.__move(barriers, doors_group)

    def offset(self) -> [int, int]:
        """смещение координат игрока на игровом поле относительно фактических координат на экране"""
        return [self.position[X] - self.rect.x,
                self.position[Y] - self.rect.y - self.rect.height + STEP]

    def set_position(self, position: [int, int]) -> None:
        self.position = position

    def draw_hp(self, screen) -> None:
        # не отображаем шкалу здоровья, если оно полное
        if self.hp == self.max_hp:
            return None
        pygame.draw.rect(screen,
                         color.GREY,
                         (self.rect.x, self.rect.y - 16, self.rect.width, 4), 0)
        pygame.draw.rect(screen,
                         color.RED,
                         (self.rect.x, self.rect.y - 16, self.rect.width * self.hp // self.max_hp, 4), 0)

    def keydown(self, key) -> None:
        if key == LEFT:
            self.key_left = True
        elif key == RIGHT:
            self.key_right = True
        elif key == UP:
            self.key_up = True
        elif key == DOWN:
            self.key_down = True

    def keyup(self, key) -> None:
        if key == LEFT:
            self.key_left = False
        elif key == RIGHT:
            self.key_right = False
        elif key == UP:
            self.key_up = False
        elif key == DOWN:
            self.key_down = False


class Inventory:
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
