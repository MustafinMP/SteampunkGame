import pygame
from geometry_abstractions import scale
from .scene_object import SceneObject
from .background_object import BackgroundObject
from .action_object import ActionObject
from const import RATIO, Keys
from camera import Camera
from player_module import player as p_module
import locations


class Scene:
    """Игровое поле. Отвечает непосредственно за игровой процесс (декорации, игроки, кнопки)."""

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
        self.camera.update(self.player)
        directory = data['directory']
        for sco in data['scene_objects']:
            sco_obj = SceneObject(self, scale(sco['position'], RATIO), directory + sco['image'],
                                  directory + sco['shadow_image'])
            self.camera.apply(sco_obj)
            self.hard_decorations.append(sco_obj)

        for bg in data['backgrounds']:
            bg_obj = BackgroundObject(self, scale(bg['position'], RATIO), directory + bg['image'])
            self.camera.apply(bg_obj)
            self.background_decorations.append(bg_obj)

        for actn in data['action_places']:
            actn_obj = ActionObject(self, scale(actn['position'], RATIO),
                                    directory + actn['image'], actn['hint_image'])
            action = self.reload_scene
            actn_obj.set_action(action, *actn['args'])
            self.action_places.append(actn_obj)
            self.camera.apply(actn_obj)

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
            if action_place.collide_shadow(self.player):
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
        self.camera.update(self.player)

        for decoration in self.background_decorations:
            self.camera.apply(decoration)
            decoration.update()
        for decoration in self.hard_decorations:
            self.camera.apply(decoration)
            decoration.update()
        for action_place in self.action_places:
            self.camera.apply(action_place)
            action_place.update()

        self.camera.apply(self.player)

    def draw(self, screen) -> None:
        for decoration in self.background_decorations:
            decoration.draw(screen)

        all_sprites = self.hard_decorations + [self.player]
        all_sprites.sort(key=lambda obj: obj.sort_key())
        for obj in all_sprites:
            obj.draw(screen)

        for redirect_zone in self.action_places:
            redirect_zone.draw(screen, draw_hint=redirect_zone.collide_shadow(self.player))
