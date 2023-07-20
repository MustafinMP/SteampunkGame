import pygame
from pygame.sprite import Sprite, Group

from const import *
import player
import load_data
import locations


class Scene:
    '''
    Игровое поле.

    Отвечает непосредственно за игровой процесс (декорации, игроки, кнопки).
    '''

    def __init__(self, game, location):
        self.game = game
        self.player_group = Group()
        self.enemies_group = Group()
        self.enemies_hp_group = Group()
        self.barriers = Group()
        self.floor_group = Group()
        self.floor_rect_group = []
        self.doors_group = Group()
        self.shadows_group = Group()
        self.redirect_zones = Group()

        location_data = locations.get(location)

        player_coord = [i * STEP for i in location_data['start_position']]
        self.player = player.Player(player_coord, self.player_group)

        self.__init_decorations(location_data)

        self.pause = False

    def __init_decorations(self, data: dict) -> None:
        offset = self.player.offset()

        for barrier in data['barriers']:
            Barrier(self.game,
                    barrier['position'],
                    barrier['name'], offset, self.barriers)

        for shadow in data['shadows']:
            Floor(self.game,
                  shadow['position'],
                  shadow['name'], offset, self.shadows_group)

        for floor in data['floor_rect']:
            self.floor_rect_group.append(FloorRect(floor['color'],
                                                   floor['position'],
                                                   floor['size'], offset))

        for redirect_zone in data['redirect_zones']:
            RedirectZone(self.game,
                         redirect_zone['position'],
                         redirect_zone['name'],
                         offset,
                         redirect_zone['redirect_to'], self.redirect_zones)

    def __find_zone_and_redirect(self):
        for redirect_zone in self.redirect_zones.sprites():
            if redirect_zone.is_collided_with(self.player.shadow):
                new_location = redirect_zone.get_redirect_address()
                self.reload_scene(new_location)
                break

    def reload_scene(self, location) -> None:
        """Используется для перезагрузки сцены при смене локации"""
        del self.enemies_group, self.enemies_hp_group, self.barriers, self.floor_group
        del self.floor_rect_group, self.doors_group, self.shadows_group, self.redirect_zones
        self.enemies_group = Group()
        self.enemies_hp_group = Group()
        self.barriers = Group()
        self.floor_group = Group()
        self.floor_rect_group = []
        self.doors_group = Group()
        self.shadows_group = Group()
        self.redirect_zones = Group()

        location_data = locations.get(location)

        player_coord = location_data['start_position']
        self.player.set_position(list(map(lambda i: i * STEP, player_coord)))

        self.__init_decorations(location_data)

        self.pause = False

    def draw(self, screen) -> None:
        for floor in self.floor_rect_group:
            floor.draw(screen)
        self.floor_group.draw(screen)
        self.shadows_group.draw(screen)
        self.barriers.draw(screen)
        self.player_group.draw(screen)
        self.enemies_group.draw(screen)
        self.player.draw_hp(screen)
        self.redirect_zones.draw(screen)
        for redirect_zone in self.redirect_zones.sprites():
            if redirect_zone.is_collided_with(self.player.shadow):
                redirect_zone.draw_hint(screen)

    def event_update(self, event) -> None:
        # обработка клавиш движения
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.player.keydown(UP)
                    case pygame.K_DOWN:
                        self.player.keydown(DOWN)
                    case pygame.K_RIGHT:
                        self.player.keydown(RIGHT)
                    case pygame.K_LEFT:
                        self.player.keydown(LEFT)
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_UP:
                        self.player.keyup(UP)
                    case pygame.K_DOWN:
                        self.player.keyup(DOWN)
                    case pygame.K_RIGHT:
                        self.player.keyup(RIGHT)
                    case pygame.K_LEFT:
                        self.player.keyup(LEFT)
        # обработка клавиш взаимодействия
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.__find_zone_and_redirect()

    def passive_update(self, size) -> None:
        self.player.passive_update(size, self.barriers, self.doors_group)
        offset = self.player.offset()

        for floor in self.floor_group.sprites():
            floor.passive_update(offset)

        for floor in self.floor_rect_group:
            floor.passive_update(offset)

        for shadow in self.shadows_group.sprites():
            shadow.passive_update(offset)

        for wall in self.barriers.sprites():
            wall.passive_update(offset)

        for r_zone in self.redirect_zones.sprites():
            r_zone.passive_update(offset)


class AbstractDecoration(Sprite):
    def __init__(self, game, position, image, offset, *group):
        super().__init__(*group)
        self.game = game
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.position = [axis * STEP for axis in position]
        self.rect.x, self.rect.y = position[X] - offset[0], position[Y] - offset[1]

    def passive_update(self, offset):
        self.rect.x = self.position[X] - offset[0]
        self.rect.y = self.position[Y] - offset[1]


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


class Floor(AbstractDecoration):
    """Объект пола, не восприимчив к столкновениям"""


class Barrier(AbstractDecoration):
    """Объект любых препятствий, восприимчив к столкновениям"""


class Door(Sprite):
    def __init__(self, game, x, y, variance, *group):
        super().__init__(*group)
        self.game = game
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


class RedirectZone(AbstractDecoration):
    def __init__(self, game, position, image, offset, redirect_address, *group):
        super().__init__(game, position, image, offset, *group)
        self.redirect_address = redirect_address
        self.hint_group = Group()
        self.hint_key = Sprite()

    def get_redirect_address(self):
        redirect_address = locations.get_key(self.redirect_address)
        return redirect_address

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw_hint(self, screen):
        return