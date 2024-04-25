import pygame
from pygame.sprite import Group
from geometry_abstractions import scale
from scene.decorations import Barrier, Floor, ActionPlace
from const import RATIO, Keys
from camera import Camera
from player_module import player
import locations


class Scene:
    '''
    Игровое поле.

    Отвечает непосредственно за игровой процесс (декорации, игроки, кнопки).
    '''

    def __init__(self, game, location):
        self.game = game

        self.hard_decorations_group = Group()
        self.background_decorations_group = Group()
        self.action_places_group = Group()
        self.all_decorations_group = Group()

        self.player_group = Group()
        self.enemies_group = Group()

        location_data = locations.get_location_data(location)

        player_coord = scale(location_data['start_position'], RATIO)
        self.player = player.PlayerSprite(self, player_coord, self.player_group)

        self.camera = Camera()

        self.__init_decorations(location_data)

        self.pause = False

    def __init_decorations(self, data: dict) -> None:
        self.camera.update(self.player)
        directory = data['directory']
        for barrier in data['barriers']:
            obj = Barrier(scale(barrier['position'], RATIO), directory + barrier['name'],
                          self.hard_decorations_group,
                          self.all_decorations_group)
            self.camera.apply(obj)

        for floor in data['floor']:
            obj = Floor(scale(floor['position'], RATIO), directory + floor['name'],
                        self.background_decorations_group,
                        self.all_decorations_group)
            self.camera.apply(obj)

        for action_place in data['action_places']:
            obj = ActionPlace(scale(action_place['position'], RATIO),
                              directory + action_place['name'], action_place['hint'], self.action_places_group,
                              self.all_decorations_group)
            action = self.reload_scene
            obj.set_action(action, *action_place['args'])
            self.camera.apply(obj)

    def __update_action_places(self):
        for action_place in self.action_places_group.sprites():
            if action_place.is_collided_with(self.player.shadow):
                action_place.call_action()
                break

    def reload_scene(self, location) -> None:
        """Используется для перезагрузки сцены при смене локации"""
        self.hard_decorations_group = Group()
        self.background_decorations_group = Group()
        self.action_places_group = Group()

        self.enemies_group = Group()

        location_data = locations.get_location_data(location)

        player_coord = location_data['start_position']
        self.player.set_position(list(map(lambda i: i * RATIO, player_coord)))

        self.__init_decorations(location_data)

        self.pause = False

    def draw(self, screen) -> None:
        self.background_decorations_group.draw(screen)
        self.hard_decorations_group.draw(screen)

        self.player_group.draw(screen)
        self.enemies_group.draw(screen)
        self.player.draw_hp(screen)

        self.action_places_group.draw(screen)
        for redirect_zone in self.action_places_group.sprites():
            if redirect_zone.is_collided_with(self.player.shadow):
                redirect_zone.draw_hint(screen)  # отрисовка подсказки по клавише

    def update_event(self, event) -> None:
        """Обработчик клавиш"""

        match event.type:  # обработка клавиш движения
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.player.keydown(Keys.UP)
                    case pygame.K_DOWN:
                        self.player.keydown(Keys.DOWN)
                    case pygame.K_RIGHT:
                        self.player.keydown(Keys.RIGHT)
                    case pygame.K_LEFT:
                        self.player.keydown(Keys.LEFT)
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_UP:
                        self.player.keyup(Keys.UP)
                    case pygame.K_DOWN:
                        self.player.keyup(Keys.DOWN)
                    case pygame.K_RIGHT:
                        self.player.keyup(Keys.RIGHT)
                    case pygame.K_LEFT:
                        self.player.keyup(Keys.LEFT)
        # обработка клавиш взаимодействия
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.__update_action_places()

    def update(self) -> None:
        self.camera.update_screen_size(self.game.screen_size)

        self.player.update(self.hard_decorations_group)
        self.camera.update(self.player)

        for decoration in self.all_decorations_group.sprites():
            self.camera.apply(decoration)
