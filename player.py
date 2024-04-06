import pygame
from pygame.sprite import Sprite, Group, collide_rect, spritecollideany
import load_data
from const import *
import color
from moving_vector import MovingVector, PlayerMovingVector


class PlayerImages:
    STAY = 0
    ATTACK = 1
    RUNNING = 2

    def __init__(self):
        self.iteration = 0
        self.ITERATION_LIMIT_RUNNING = 4 * ANIMATION_FPS
        # формируем таблицы изображений
        self.main_image = load_data.load_image('player.png')
        self.stay = [
            self.main_image,
            self.main_image,
            self.main_image,
            self.main_image
        ]
        # таблица для бега
        self.running_up = []
        self.running_down = [
            load_data.load_image('running_down_1.png'),
            self.main_image,
            load_data.load_image('running_down_3.png'),
            self.main_image
        ]
        self.running_right = []
        self.running_left = []
        self.running = {DOWN: self.running_down}

        self.last_move_type = self.STAY
        self.last_direction = DOWN

    def direction(self, vx, vy):
        if vx > 0:
            return RIGHT
        if vx < 0:
            return LEFT
        if vy > 0:
            return DOWN
        if vy < 0:
            return UP

    def update_image(self, move_type, vx=0, vy=0):
        if move_type == self.STAY:
            self.iteration = 0
            self.last_move_type = self.STAY
            return self.main_image

        direction = self.direction(vx, vy)

        # сброс счетчика итераций при смене типа движений
        if self.last_move_type != move_type:
            self.iteration = 0

        if move_type == self.RUNNING:
            self.iteration += 1
            if self.iteration == self.ITERATION_LIMIT_RUNNING:
                self.iteration = 0
            self.last_move_type = self.RUNNING
            return self.running[direction][self.iteration // ANIMATION_FPS]


class PlayerData:
    def __init__(self):
        self.hp = 10
        self.max_hp = 10

        self.inventory = Inventory()


class PlayerSprite(Sprite):
    """Главный класс персонажа.
    Хранит все сведения об нем (позиция на поле, анимации, сценарные характеристики, такие как здоровье), и т.д."""

    def __init__(self, game_position: (int, int), *group) -> None:
        super().__init__(*group)
        self.image = PlayerImages().main_image
        self.images = PlayerImages()

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.game_position = game_position
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
            self.game_position[X] += self.mv.x
        self.shadow.rect.x -= self.mv.x

        self.shadow.rect.y += self.mv.y
        if not spritecollideany(self.shadow, barriers):
            self.game_position[Y] += self.mv.y
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

    def passive_update(self, size, barriers) -> None:
        self.__update_shadow_coord()
        self.mv.update()
        self.__move(barriers)

        # self.__update_image()

    def set_position(self, game_position: (int, int)) -> None:
        self.game_position = game_position

    def draw_hp(self, screen) -> None:
        # не отображаем шкалу здоровья, если оно полное
        if self.data.hp == self.data.max_hp:
            return None
        pygame.draw.rect(screen,
                         color.GREY,
                         (self.rect.x, self.rect.y - 16, self.rect.width, 4), 0)
        pygame.draw.rect(screen,
                         color.RED,
                         (self.rect.x, self.rect.y - 16, self.rect.width * self.data.hp // self.data.max_hp, 4), 0)

    def keydown(self, key) -> None:
        self.mv.keydown(key)

    def keyup(self, key) -> None:
        self.mv.keyup(key)


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
