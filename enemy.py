import pygame
from pygame.sprite import Sprite, Group, collide_rect, spritecollideany
import load_data
from const import *


class AbstractEnemy(Sprite):
    def __init__(self, x, y, variance, image, *group):
        super().__init__(*group)
        # self.image = load_data.load_image('knight_f_idle_anim_f0.png')
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.position = {'x': x, 'y': y}
        self.rect.x, self.rect.y = x - variance[0], y - variance[1]

        self.hp = int()
        self.max_hp = int()
        self.loot = list()
        self.attack_interval = FPS

    def take_damage(self, damage, game):
        self.hp -= damage
        if self.hp <= 0:
            # TODO: create game event
            self.kill()

    def drop(self):
        return self.loot

    def passive_update(self, offset):
        self.rect.x = self.position['x'] - offset[0]
        self.rect.y = self.position['y'] - offset[1]

    def draw_hp(self, screen):
        pygame.draw.rect(screen,
                         (100, 100, 100),
                         (self.rect.x, self.rect.y - 16, self.rect.width, 4), 0)
        pygame.draw.rect(screen,
                         (180, 0, 0),
                         (self.rect.x, self.rect.y - 16, self.rect.width * self.hp // self.max_hp, 4), 0)

