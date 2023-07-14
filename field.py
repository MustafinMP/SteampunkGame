import pygame
from pygame.sprite import Sprite, Group
from const import *
import player
import load_data
import locations


class GameField:
    '''
    Игровое поле.

    Отвечает непосредственно за игровой процесс (декорации, игроки, кнопки).
    '''

    def __init__(self, location):
        super().__init__()
        self.player_group = Group()
        self.enemies_group = Group()
        self.enemies_hp_group = Group()
        self.walls_group = Group()
        self.floor_group = Group()
        self.floor_rect_group = []
        self.doors_group = Group()

        location_data = locations.get(location)

        self.player_coord = location_data['start_coord']
        self.player = player.Player(list(map(lambda i: i * STEP, self.player_coord)),
                                    self.player_group)

        offset = self.player.offset()
        # for floor_group in location_data['floor'].keys():
        #     for coords in location_data['floor'][floor_group]:
        #         Floor(coords[0] * STEP, coords[1] * STEP, floor_group + '.png', variance,  self.floor_group)

        for wall in location_data['walls']:
            Wall(wall['coord'][0] * STEP, wall['coord'][1] * STEP, wall['name'], offset, self.walls_group)

        for floor in location_data['floor_rect']:
            self.floor_rect_group.append(FloorRect(floor['color'], floor['position'], floor['size'], offset))

    def draw(self, screen):
        for floor in self.floor_rect_group:
            floor.draw(screen)
        self.floor_group.draw(screen)
        self.walls_group.draw(screen)
        self.player_group.draw(screen)
        self.enemies_group.draw(screen)
        self.player.draw_hp(screen)

    def event_update(self, game, event):
        match event.type:

            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.player.update_vector('y', - SPEED)
                    case pygame.K_DOWN:
                        self.player.update_vector('y', SPEED)
                    case pygame.K_RIGHT:
                        self.player.update_vector('x', SPEED)
                    case pygame.K_LEFT:
                        self.player.update_vector('x', - SPEED)

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_UP:
                        self.player.stop_vector('y')
                    case pygame.K_DOWN:
                        self.player.stop_vector('y')
                    case pygame.K_RIGHT:
                        self.player.stop_vector('x')
                    case pygame.K_LEFT:
                        self.player.stop_vector('x')

    def passive_update(self, size):
        self.player.passive_update(size, self.walls_group, self.doors_group)
        offset = self.player.offset()

        for floor in self.floor_group.sprites():
            floor.passive_update(offset)

        for floor in self.floor_rect_group:
            floor.passive_update(offset)

        for wall in self.walls_group.sprites():
            wall.passive_update(offset)


class FloorRect:
    def __init__(self, color, position, size, offset):
        self.color = color
        self.position = [axis * STEP for axis in position]
        self.coord = [0, 0]
        self.passive_update(offset)
        self.size = [axis * STEP for axis in size]

    def draw(self, screen):
        pygame.draw.rect(screen,
                         self.color,
                         (self.coord[0], self.coord[1], self.size[0], self.size[1]), 0)

    def passive_update(self, offset):
        self.coord[0] = self.position[0] - offset[0]
        self.coord[1] = self.position[1] - offset[1]


class Floor(Sprite):
    def __init__(self, x, y, image, offset, *group):
        super().__init__(*group)
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.position = {'x': x, 'y': y}
        self.rect.x, self.rect.y = x - offset[0], y - offset[1]

    def passive_update(self, offset):
        self.rect.x = self.position['x'] - offset[0]
        self.rect.y = self.position['y'] - offset[1]


class Wall(Sprite):
    def __init__(self, x, y, image, offset, *group):
        super().__init__(*group)
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.position = {'x': x, 'y': y}
        self.rect.x, self.rect.y = x - offset[0], y - offset[1]

    def passive_update(self, offset):
        self.rect.x = self.position['x'] - offset[0]
        self.rect.y = self.position['y'] - offset[1]


class Door(Sprite):
    def __init__(self, x, y, variance, *group):
        super().__init__(*group)
        self.images = {False: load_data.load_image('closed_door.png'),
                       True: load_data.load_image('opened_door.png')}
        self.image = self.images[False]
        self.rect = self.image.get_rect()
        self.position = {'x': x, 'y': y}
        self.rect.x, self.rect.y = x - variance[0], y - variance[1]
        self.is_opened = False

    def ping_the_door(self):
        self.is_opened = not self.is_opened
        self.image = self.images[self.is_opened]
