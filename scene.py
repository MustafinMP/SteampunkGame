import pygame
from pygame import Rect
from pygame.sprite import Sprite, Group

from const import *
from camera import Camera
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

        self.barriers = Group()
        self.floor_group = Group()
        self.redirect_zones = Group()
        self.all_decorations = Group()

        self.player_group = Group()
        self.enemies_group = Group()

        location_data = locations.get(location)

        player_coord = [i * STEP for i in location_data['start_position']]
        self.player = player.Player(player_coord, self.player_group)

        self.camera = Camera()

        self.__init_decorations(location_data)

        self.pause = False

    def __init_decorations(self, data: dict) -> None:
        self.camera.update(self.player)

        for barrier in data['barriers']:
            obj = Barrier(barrier['position'], barrier['name'], self.barriers, self.all_decorations)
            self.camera.apply(obj)

        for floor in data['floor']:
            obj = Floor(floor['position'], floor['name'], self.floor_group, self.all_decorations)
            self.camera.apply(obj)

        for redirect_zone in data['redirect_zones']:
            obj = RedirectZone(redirect_zone['position'], redirect_zone['name'], redirect_zone['redirect_to'],
                               self.redirect_zones, self.all_decorations)
            self.camera.apply(obj)

    def __redirect(self):
        for redirect_zone in self.redirect_zones.sprites():
            if redirect_zone.is_collided_with(self.player.shadow):
                new_location = redirect_zone.get_redirect_address()
                self.reload_scene(new_location)
                break

    def reload_scene(self, location) -> None:
        """Используется для перезагрузки сцены при смене локации"""
        self.barriers = Group()
        self.floor_group = Group()
        self.redirect_zones = Group()

        self.enemies_group = Group()

        location_data = locations.get(location)

        player_coord = location_data['start_position']
        self.player.set_position(list(map(lambda i: i * STEP, player_coord)))

        self.__init_decorations(location_data)

        self.pause = False

    def draw(self, screen) -> None:
        self.floor_group.draw(screen)
        self.barriers.draw(screen)
        self.player_group.draw(screen)
        self.enemies_group.draw(screen)
        self.player.draw_hp(screen)
        self.redirect_zones.draw(screen)
        for redirect_zone in self.redirect_zones.sprites():
            if redirect_zone.is_collided_with(self.player.shadow):
                redirect_zone.draw_hint(screen)

    def event_update(self, event) -> None:
        """Обработчик клавиш"""

        match event.type:  # обработка клавиш движения
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
                self.__redirect()

    def passive_update(self, size) -> None:
        self.player.passive_update(size, self.barriers)
        self.camera.update(self.player)

        for decoration in self.all_decorations.sprites():
            self.camera.apply(decoration)


class AbstractDecoration(Sprite):
    def __init__(self, position, image, *group):
        super().__init__(*group)
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.position = [axis * STEP for axis in position]
        self.rect.x, self.rect.y = position


class Floor(AbstractDecoration):
    """Объект пола, не восприимчив к столкновениям"""


class Barrier(AbstractDecoration):
    """Объект любых препятствий, восприимчив к столкновениям"""


class RedirectZone(AbstractDecoration):
    """Особый объект пола, может сменять текущую локацию"""

    def __init__(self, position, image, redirect_address, *group):
        super().__init__(position, image, *group)
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
