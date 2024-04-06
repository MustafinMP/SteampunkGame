import pygame, sys, os

from buttons import *
# import scene
import menu
from const import *

screen_size = width, height = WIDTH, HEIGHT
pygame.init()
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
lst = []


class Game:
    """Главный класс всей игры."""

    def __init__(self):
        self.widget = menu.StartMenu(self)

    def draw(self):
        self.widget.draw(screen)

    def event_update(self, event):
        """Обработка действий игрока"""
        self.widget.update_event(event)

    def update(self, screen_size: (int, int)):
        self.widget.update(screen_size)

    def redirect_to(self, object_):
        self.widget = object_

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        screen.fill((0, 0, 0))

        # контроль текущего размера экрана для правильного отображения объектов
        new_screen_size: (int, int) = pygame.display.get_window_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            game.event_update(event)  # обновление событий
        game.update(screen_size)  # обновление независимо от событий
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
