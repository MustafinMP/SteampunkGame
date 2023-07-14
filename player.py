import pygame
from pygame.sprite import Sprite, Group, collide_rect, spritecollideany
import load_data
from const import *
import color


x, y = 0, 1


class Player(Sprite):
    def __init__(self, position: list, *group) -> None:
        super().__init__(*group)
        self.image = load_data.load_image('player_x3.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [WIDTH // 2 - self.rect.width // 2,
                                    HEIGHT // 2 - self.rect.height // 2]
        self.position = position
        self.vector_x = 0
        self.vector_y = 0
        self.shadow = None
        self.init_shadow(*group)

        self.inventory = Inventory()

        self.hp = 10
        self.max_hp = 10

    def init_shadow(self, *group) -> None:
        self.shadow = Sprite(*group)
        self.shadow.image = load_data.load_image('shadow.png')
        self.shadow.rect = self.shadow.image.get_rect()
        self.update_shadow_coord()

    def update_shadow_coord(self) -> None:
        self.shadow.rect.x = self.rect.x
        self.shadow.rect.y = self.rect.y + self.rect.height // 3 * 2

    def passive_update(self, size, barriers, doors_group) -> None:
        global x, y
        w, h = size
        self.rect.x, self.rect.y = [w // 2 - self.rect.width // 2,
                                    h // 2 - self.rect.height // 2]

        self.update_shadow_coord()

        # проверяем возможность перемещения по оси X
        self.shadow.rect.x += self.vector_x
        if not (spritecollideany(self.shadow, barriers) or self.collide_doors(doors_group)):
            self.position[x] += self.vector_x
        self.shadow.rect.x -= self.vector_x

        # проверяем возможность перемещения по оси Y
        self.shadow.rect.y += self.vector_y
        if not (spritecollideany(self.shadow, barriers) or self.collide_doors(doors_group)):
            self.position[y] += self.vector_y
        self.shadow.rect.y -= self.vector_y

    def offset(self) -> [int, int]:
        """смещение координат игрока на игровом поле относительно фактических координат на экране"""
        return [self.position[x] - self.rect.x,
                self.position[y] - self.rect.y - self.rect.height + STEP]

    def update_vector(self, axis: str, speed: int) -> None:
        """Направление движения игрока в пространстве"""
        match axis:
            case 'x':
                if self.vector_x == 0 or speed == self.vector_x:
                    self.vector_x = speed
            case 'y':
                if self.vector_y == 0 or speed == self.vector_y:
                    self.vector_y = speed

    def stop_vector(self, axis: str) -> None:
        match axis:
            case 'x':
                self.vector_x = 0
            case 'y':
                self.vector_y = 0

    def collide_doors(self, doors_group: Group) -> bool:
        return any([not door.is_opened and collide_rect(self, door) for door in doors_group])

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


class Inventory:
    def __init__(self):
        self.inventory = dict()

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
        return 0


class HpDisplay:
    pass  # TODO: сделать класс для отображения ХП
