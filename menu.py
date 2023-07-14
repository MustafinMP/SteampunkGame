import pygame
from pygame.sprite import Sprite, Group
import sys
from buttons import AbstractActionButton
from scene import Scene
import load_data
from locations import GARAGE


def terminate():
    pygame.quit()
    sys.exit()


class AbstractMenu:
    def __init__(self):
        self.buttons = Group()

    def draw(self, screen):
        self.buttons.draw(screen)

    def update(self, args):
        self.buttons.update(args)

    def event_update(self, game, event):
        for button in self.buttons:
            button.event_update(game, event)

    def passive_update(self, size):
        pass


class StartMenu(AbstractMenu):
    class StartButton(AbstractActionButton):
        def event_update(self, game, event):
            super().event_update(game, event)
            if self.pressed:
                game.redirect_to(Scene(GARAGE))

    class ExitButton(AbstractActionButton):
        def event_update(self, game, event):
            super().event_update(game, event)
            if self.pressed:
                game.terminate()

    def __init__(self):
        super().__init__()
        self.start_button = self.StartButton(400, 100, 'start_button.png', 'start_button.png', self.buttons)
        self.exit_button = self.ExitButton(400, 400, 'exit_button.png', 'exit_button.png', self.buttons)


