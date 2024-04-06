import main
from buttons import ActionButtonsGroup


class Widget:
    def __init__(self, game: main.Game):
        self.game: main.Game = game
        self.action_buttons = ActionButtonsGroup()

    def update_event(self, event):
        self.action_buttons.update_event(event)

    def update(self, screen_size: (int, int)):
        pass

    def draw(self, screen):
        self.action_buttons.draw(screen)