import pygame
from pygame.sprite import Sprite, Group
import sys

import main
from buttons import ActionButton
import scene
import load_data
from locations import GARAGE
import widget


def terminate():
    pygame.quit()
    sys.exit()


class AbstractMenu:
    def __init__(self, game):
        self.buttons = Group()
        self.game = game

    def draw(self, screen):
        self.buttons.draw(screen)

    def update(self, args):
        self.buttons.update(args)

    def passive_update(self, size):
        pass


class StartMenu(widget.Widget):
    class StartButton(ActionButton):
        def call(self):
            self.widget.redirect_to_garage()

    class ExitButton(ActionButton):
        def call(self):
            self.widget.terminate_game()

    def __init__(self, game: main.Game):
        super().__init__(game)
        self.start_button = self.StartButton(self, (400, 100),
                                             'start_button.png', 'start_button.png',
                                             self.action_buttons)
        self.exit_button = self.ExitButton(self, (400, 400),
                                           'exit_button.png', 'exit_button.png',
                                           self.action_buttons)

    def update(self, screen_size: (int, int)):
        sc_x, sc_y = screen_size
        self.start_button.set_coord((sc_x // 2 - 200, (sc_y - 400) // 3))
        self.exit_button.set_coord((sc_x // 2 - 200, (sc_y - 400) // 3 * 2 + 200))

    def redirect_to_garage(self):
        self.game.redirect_to(scene.Scene(self.game, GARAGE))

    def terminate_game(self):
        self.game.terminate()
