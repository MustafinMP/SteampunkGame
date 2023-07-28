import pygame
from pygame.sprite import Sprite, Group, collide_rect, spritecollideany
import load_data
from const import *
import color


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


class Player(Sprite):
    """Главный класс персонажа.
    Хранит все сведения об нем (позиция на поле, анимации, сценарные характеристики, такие как здоровье), и т.д."""

    def __init__(self, position: list, *group) -> None:
        super().__init__(*group)
        self.images = PlayerImages()
        self.image = self.images.main_image

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [WIDTH // 2 - self.rect.width // 2,
                                    HEIGHT // 2 - self.rect.height // 2]
        # положение на игровом поле
        self.position = position
        self.vx = 0
        self.vy = 0
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

    def __move(self, barriers: Group) -> None:
        """Меняем позицию игрока, если это возможно"""
        self.shadow.rect.x += self.vx
        if not spritecollideany(self.shadow, barriers):
            self.position[X] += self.vx
        self.shadow.rect.x -= self.vx

        self.shadow.rect.y += self.vy
        if not spritecollideany(self.shadow, barriers):
            self.position[Y] += self.vy
        self.shadow.rect.y -= self.vy

    def __update_image(self):
        if self.vx == 0 and  self.vy == 0:
            image = self.images.update_image(self.images.STAY)
        else:
            image = self.images.update_image(self.images.RUNNING, self.vx, self.vy)
        self.image = image

    def __update_shadow_coord(self) -> None:
        self.shadow.rect.x = self.rect.x
        self.shadow.rect.y = self.rect.y + self.rect.height // 3 * 2

    def __update_vectors(self) -> None:
        """Направление движения игрока в пространстве"""
        # update X vector
        if self.key_right == self.key_left:
            self.vx = 0
        elif self.key_right and not self.key_left:
            self.vx = SPEED
        elif self.key_left and not self.key_right:
            self.vx = -SPEED
        # update Y vector
        if self.key_up == self.key_down:
            self.vy = 0
        elif self.key_up and not self.key_down:
            self.vy = -SPEED
        elif self.key_down and not self.key_up:
            self.vy = SPEED

    def passive_update(self, size, barriers) -> None:
        w, h = size
        self.rect.x, self.rect.y = [w // 2 - self.rect.width // 2,
                                    h // 2 - self.rect.height // 2]
        self.__update_shadow_coord()
        self.__update_vectors()
        self.__move(barriers)

        self.__update_image()

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
