import load_data
from const import *


class PlayerImageController:
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
        self.running = {DOWN: self.running_down,
                        UP: self.running_down,
                        LEFT: self.running_down,
                        RIGHT: self.running_down}

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

        # сброс счетчика итераций при смене типа движений
        if self.last_move_type != move_type:
            self.iteration = 0

        if move_type == self.RUNNING:
            self.iteration += 1
            if self.iteration == self.ITERATION_LIMIT_RUNNING:
                self.iteration = 0
            self.last_move_type = self.RUNNING

            direction = self.direction(vx, vy)
            return self.running[direction][self.iteration // ANIMATION_FPS]
