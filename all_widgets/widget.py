import main
from all_widgets.buttons import ActionButtonsGroup
from const import Colors, Color


class Widget:
    """Базовый класс всех виджетов"""
    def __init__(self, game: main.Game) -> None:
        self.game: main.Game = game
        self.action_buttons = ActionButtonsGroup()
        self.background_color: Color = Colors.default

    def update_event(self, event) -> None:
        self.action_buttons.update_event(event)

    def update(self) -> None:
        pass

    def draw(self, screen) -> None:
        self.action_buttons.draw(screen)