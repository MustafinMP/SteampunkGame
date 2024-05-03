import main
from all_widgets.buttons import ActionButton
from locations import GARAGE
from all_widgets import widget
from scene import scene
from progress_storage import ProgressStorage


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
        if ProgressStorage.have_containers():
            container_name = ProgressStorage.last_container()
            self.game.redirect_to(ProgressStorage.load_progress(self.game, container_name))
            return
        self.game.redirect_to(scene.Scene(self.game, GARAGE))

    def terminate_game(self) -> None:
        self.game.terminate()
