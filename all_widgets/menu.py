import main
from all_widgets.buttons import ActionButton
from locations import GARAGE
from all_widgets import widget, scene


class StartMenu(widget.Widget):
    def __init__(self, game: main.Game):
        super().__init__(game)
        self.start_button = ActionButton(self, (400, 100), 'start_button.png',
                                         'start_button.png', self.action_buttons)
        self.exit_button = ActionButton(self, (400, 400), 'exit_button.png',
                                        'exit_button.png', self.action_buttons)

        self.start_button.set_action(self.redirect_to_garage)
        self.exit_button.set_action(self.terminate_game)

    def update(self):
        sc_x, sc_y = self.game.screen_size
        self.start_button.set_coord((sc_x // 2 - 200, (sc_y - 400) // 3))
        self.exit_button.set_coord((sc_x // 2 - 200, (sc_y - 400) // 3 * 2 + 200))

    def redirect_to_garage(self):
        """Перемещение в стартовую сцену"""
        self.game.redirect_to(scene.Scene(self.game, GARAGE))

    def terminate_game(self):
        self.game.terminate()
