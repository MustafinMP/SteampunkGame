import pygame, sys, os

from buttons import *
from scene import *
from menu import *
from const import *

size = width, height = WIDTH, HEIGHT
pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
screen.fill((0, 0, 0))
clock = pygame.time.Clock()
lst = []


class Game:
    """Главный класс всей игры."""

    def __init__(self):
        self.widget = StartMenu(self)

    def draw(self):
        self.widget.draw(screen)

    def event_update(self, event):
        """Обработка действий игрока"""
        self.widget.event_update(event)

    def passive_update(self, size):
        self.widget.passive_update(size)

    def redirect_to(self, object_):
        self.widget = object_

    def terminate(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    game = Game()
    running = True
    while running:
        screen.fill((0, 0, 0))

        # контроль текущего размера экрана для правильного отображения объектов
        size = width, height = pygame.display.get_window_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            game.event_update(event)  # обновление событий
        game.passive_update(size)  # обновление независимо от событий
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
