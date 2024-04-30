import pygame
from geometry_abstractions import scale
from scene.decorations import Floor, ActionPlace
from scene.scene_object import SceneObject
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

        self.hard_decorations = []
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
        self.camera.update(self.player.main_sprite)
        directory = data['directory']
        for barrier in data['barriers']:
            obj = SceneObject(self, scale(barrier['position'], RATIO), directory + barrier['image'],
                              directory + barrier['shadow_image'])
            self.camera.apply(obj.main_sprite)
            self.hard_decorations.append(obj)

        for floor in data['floor']:
            obj = Floor(self, scale(floor['position'], RATIO), directory + floor['image'])
            self.camera.apply(obj)
            self.background_decorations.append(obj)

        for action_place in data['action_places']:
            obj = ActionPlace(self, scale(action_place['position'], RATIO),
                              directory + action_place['image'], action_place['hint_image'])
            action = self.reload_scene
            obj.set_action(action, *action_place['args'])
            self.action_places.append(obj)
            self.camera.apply(obj)

    def reload_scene(self, location_name: str) -> None:
        """Используется для перезагрузки сцены при смене локации"""
        self.hard_decorations = []
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
        self.player.update(self.hard_decorations)
        self.camera.update(self.player.main_sprite)

        for decoration in self.background_decorations:
            self.camera.apply(decoration)
        for decoration in self.hard_decorations:
            self.camera.apply(decoration.main_sprite)
            decoration.update()
        for action_place in self.action_places:
            self.camera.apply(action_place)
            
        self.camera.apply(self.player.main_sprite)

    def draw(self, screen) -> None:
        for decoration in self.background_decorations:
            decoration.draw(screen)

        all_sprites = self.hard_decorations + [self.player]
        all_sprites.sort(key=lambda obj: obj.sort_key())
        for obj in all_sprites:
            obj.draw(screen)

        for redirect_zone in self.action_places:
            redirect_zone.draw(screen, draw_hint=redirect_zone.is_collided_with(self.player.shadow_sprite))
