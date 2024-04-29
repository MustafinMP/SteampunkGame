import pygame
from pygame.sprite import Group
from geometry_abstractions import scale
from scene.decorations import Barrier, Floor, ActionPlace
from const import RATIO, Keys
from camera import Camera
from player_module import player as p_module
import locations


class Scene:
    '''
    Игровое поле. Отвечает непосредственно за игровой процесс (декорации, игроки, кнопки).
    '''

    def __init__(self, game, location) -> None:
        self.game = game

        self.hard_decorations_group = Group()
        self.background_decorations = []
        self.action_places = []

        location_data = locations.get_location_data(location)

        player_position = scale(location_data['start_position'], RATIO)
        self.player = p_module.Player(self)
        self.player.set_position(player_position)

        self.camera = Camera()

        self.__init_decorations(location_data)

        self.pause = False

    def __init_decorations(self, data: dict) -> None:
        self.camera.update(self.player.player_sprite)
        directory = data['directory']
        for barrier in data['barriers']:
            obj = Barrier(self, scale(barrier['position'], RATIO), directory + barrier['name'],
                          self.hard_decorations_group)
            self.camera.apply(obj)

        for floor in data['floor']:
            obj = Floor(self, scale(floor['position'], RATIO), directory + floor['name'])
            self.camera.apply(obj)
            self.background_decorations.append(obj)

        for action_place in data['action_places']:
            obj = ActionPlace(self, scale(action_place['position'], RATIO),
                              directory + action_place['name'], action_place['hint'])
            action = self.reload_scene
            obj.set_action(action, *action_place['args'])
            self.action_places.append(obj)
            self.camera.apply(obj)

    def reload_scene(self, location_name: str) -> None:
        """Используется для перезагрузки сцены при смене локации"""
        self.hard_decorations_group = Group()
        self.background_decorations = []
        self.action_places = []

        location_data = locations.get_location_data(location_name)

        player_coord = location_data['start_position']
        self.player.set_position(list(map(lambda i: i * RATIO, player_coord)))

        self.__init_decorations(location_data)

        self.pause = False

    def __update_action_places(self) -> None:
        for action_place in self.action_places:
            if action_place.is_collided_with(self.player.shadow_sprite):
                action_place.call_action()
                break

    def update_event(self, event) -> None:
        """Обработчик клавиш"""
        move_keys = {
            pygame.K_UP: Keys.UP,
            pygame.K_DOWN: Keys.DOWN,
            pygame.K_RIGHT: Keys.RIGHT,
            pygame.K_LEFT: Keys.LEFT,
        }
        if event.type == pygame.KEYDOWN:
            if event.key in move_keys.keys():
                self.player.keydown(move_keys[event.key])
            if event.key == pygame.K_a:  # обработка клавиш взаимодействия
                self.__update_action_places()

        elif event.type == pygame.KEYUP:
            if event.key in move_keys.keys():
                self.player.keyup(move_keys[event.key])

    def update(self) -> None:
        self.camera.update_screen_size(self.game.screen_size)
        self.player.update(self.hard_decorations_group)
        self.camera.update(self.player.player_sprite)
        for decoration in self.background_decorations:
            self.camera.apply(decoration)
        for decoration in self.hard_decorations_group.sprites():
            self.camera.apply(decoration)
        for action_place in self.action_places:
            self.camera.apply(action_place)
        self.camera.apply(self.player.player_sprite)

    def draw(self, screen) -> None:
        for decoration in self.background_decorations:
            decoration.draw(screen)
        self.hard_decorations_group.draw(screen)

        self.player.draw(screen)

        for redirect_zone in self.action_places:
            redirect_zone.draw(screen, draw_hint=redirect_zone.is_collided_with(self.player.shadow_sprite))
