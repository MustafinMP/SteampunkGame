import pygame
import sys

import load_data
from all_widgets import menu
from scene.scene import Scene
from const import WIDTH, HEIGHT, FPS, Colors, Color
from progress_storage import ProgressStorage

screen_size: tuple[int, int]
screen_size = width, height = WIDTH, HEIGHT
pygame.init()
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

screen.fill(Colors.default)
clock = pygame.time.Clock()


class Game:
    """Главный класс всей игры."""

    def __init__(self) -> None:
        self.widget = menu.StartMenu(self)
        self.screen_size: tuple[int, int] = screen_size

    def draw(self) -> None:
        self.widget.draw(screen)

    def event_update(self, event) -> None:
        """Обработка действий игрока"""
        self.widget.update_event(event)

    def update(self) -> None:
        self.widget.update()

    def update_screen_size(self, new_screen_size: list[int, int] | tuple[int, int]) -> None:
        self.screen_size = new_screen_size

    def redirect_to(self, widget) -> None:
        self.widget = widget

    def background_color(self) -> Color:
        return self.widget.background_color

    def save_game(self):
        ProgressStorage.save_progress(self.widget)

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()


def run() -> None:
    game = Game()
    running = True
    while running:
        screen.fill(Colors.default)

        # контроль текущего размера экрана для правильного отображения объектов
        new_screen_size: list[int, int] = pygame.display.get_window_size()
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


if __name__ == '__main__':
    run()
