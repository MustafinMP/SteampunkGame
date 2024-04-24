import pygame
import main
from all_widgets.buttons import ActionButton, KeyAction, Group
from locations import GARAGE
from all_widgets import widget, scene
from const import Colors


class KeyMenu(widget.Widget):
    """С этим меню можно взаимодействовать только клавиатурой"""

    def __init__(self, game: main.Game):
        super().__init__(game)
        del self.action_buttons
        self.sprite_group = Group()
        self.actions: list[KeyAction] = []
        self.actions_count: int = 0
        self.current_action_index = 0

    def update_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.actions[self.current_action_index].set_status(False)
                self.current_action_index -= 1
                if self.current_action_index < 0:
                    self.current_action_index = self.actions_count - 1
                self.actions[self.current_action_index].set_status(True)

            elif event.key == pygame.K_DOWN:
                self.actions[self.current_action_index].set_status(False)
                self.current_action_index += 1
                if self.current_action_index == self.actions_count:
                    self.current_action_index = 0
                self.actions[self.current_action_index].set_status(True)

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.actions[self.current_action_index].call()


class KeyStartMenu(KeyMenu):
    def __init__(self, game: main.Game):
        super().__init__(game)
        self.background_color = Colors.dark_grey
        self.actions = [
            KeyAction(self, (400, 100), 'buttons/current_play_button.png',
                      'buttons/not_current_play_button.png', self.sprite_group,
                      action=self.redirect_to_garage),
            KeyAction(self, (400, 250), 'buttons/current_exit_button.png',
                      'buttons/not_current_exit_button.png', self.sprite_group,
                      action=self.terminate_game)
        ]
        self.actions[0].set_status(True)
        self.actions_count = 2

    def redirect_to_garage(self):
        """Перемещение в стартовую сцену"""
        self.game.redirect_to(scene.Scene(self.game, GARAGE))

    def terminate_game(self):
        self.game.terminate()

    def update(self):
        sc_x, sc_y = self.game.screen_size
        self.actions[0].set_coord((sc_x // 2 - 200, (sc_y - 400) // 2))
        self.actions[1].set_coord((sc_x // 2 - 200, (sc_y - 400) // 2 + 150))

    def draw(self, screen):
        self.sprite_group.draw(screen)