import pygame
import sys
from all_widgets import menu
from const import *

screen_size = width, height = WIDTH, HEIGHT
pygame.init()
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

background_color = (20, 20, 20)

screen.fill(background_color)
clock = pygame.time.Clock()


class Game:
    """Главный класс всей игры."""

    def __init__(self):
        self.widget = menu.StartMenu(self)
        self.screen_size = screen_size

    def draw(self):
        self.widget.draw(screen)

    def event_update(self, event):
        """Обработка действий игрока"""
        self.widget.update_event(event)

    def update(self):
        self.widget.update()

    def update_screen_size(self, new_screen_size: (int, int)):
        self.screen_size = new_screen_size

    def redirect_to(self, object_):
        self.widget = object_

    @staticmethod
    def terminate():
        terminate()


def run() -> None:
    game = Game()
    running = True
    while running:
        screen.fill(background_color)

        # контроль текущего размера экрана для правильного отображения объектов
        new_screen_size: (int, int) = pygame.display.get_window_size()
        if game.screen_size != new_screen_size:
            game.update_screen_size(new_screen_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            game.event_update(event)  # обновление событий
        game.update()  # обновление независимо от событий
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run()
