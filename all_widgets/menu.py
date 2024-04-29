import pygame
import main
from all_widgets.buttons import KeyAction, Group, ActionButton
from locations import GARAGE
from all_widgets import widget
from scene import scene
from const import Colors


class KeyMenu(widget.Widget):
    """С этим меню можно взаимодействовать только клавиатурой"""

    def __init__(self, game: main.Game) -> None:
        super().__init__(game)
        del self.action_buttons
        self.sprite_group = Group()
        self.actions: list[KeyAction] = []
        self.actions_count: int = 0
        self.current_action_index = 0

    def update_event(self, event) -> None:
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


class StartMenu(widget.Widget):
    def __init__(self, game: main.Game) -> None:
        super().__init__(game)
        self.start_button = ActionButton(self,
                                         'buttons/play_button.png',
                                         'buttons/play_button.png',
                                         self.action_buttons)
        self.start_button.set_coord((400, 100))
        self.start_button.set_action(self.redirect_to_garage)

        self.exit_button = ActionButton(self,
                                        'buttons/exit_button.png',
                                        'buttons/exit_button.png',
                                        self.action_buttons)
        self.exit_button.set_coord((400, 400))
        self.exit_button.set_action(self.terminate_game)

    def update(self) -> None:
        sc_x, sc_y = self.game.screen_size
        self.start_button.set_coord((sc_x // 2 - 200, (sc_y - 400) // 3))
        self.exit_button.set_coord((sc_x // 2 - 200, (sc_y - 400) // 3 * 2 + 200))

    def redirect_to_garage(self) -> None:
        """Перемещение в стартовую сцену"""
        self.game.redirect_to(scene.Scene(self.game, GARAGE))

    def terminate_game(self) -> None:
        self.game.terminate()
