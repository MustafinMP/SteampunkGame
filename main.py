import pygame
import sys
from all_widgets import menu
from const import WIDTH, HEIGHT, FPS, Colors, Color

screen_size = width, height = WIDTH, HEIGHT
pygame.init()
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

screen.fill(Colors.default)
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

    def redirect_to(self, widget_):
        self.widget = widget_

    def background_color(self) -> Color:
        return self.widget.background_color

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
