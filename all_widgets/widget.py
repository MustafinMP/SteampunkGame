import main
from all_widgets.buttons import ActionButtonsGroup


class Widget:
    """Базовый класс всех виджетов"""
    def __init__(self, game: main.Game):
        self.game: main.Game = game
        self.action_buttons = ActionButtonsGroup()

    def update_event(self, event):
        self.action_buttons.update_event(event)

    def update(self):
        pass

    def draw(self, screen):
        self.action_buttons.draw(screen)