from pygame.sprite import Sprite, Group
import pygame
import load_data


class ActionButtonsGroup(Group):
    def update_event(self, event):
        for button in self.sprites():
            if event.type == pygame.MOUSEBUTTONDOWN and button.collide(event.pos):
                button.click()
            elif event.type == pygame.MOUSEBUTTONUP:
                button.leave()


class ActionButton(Sprite):
    def __init__(self, widget, coord: (int, int), pressed_image, not_pressed_image, *group):
        super().__init__(*group)

        self.widget = widget

        self.images = {True: load_data.load_image(pressed_image),
                       False: load_data.load_image(not_pressed_image)
                       }
        self.pressed = False
        self.image = self.images[self.pressed]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord
        self.action_func = lambda: ...

    def set_coord(self, new_coord: (int, int)) -> None:
        self.rect.x, self.rect.y = new_coord

    def set_action(self, func: object) -> None:
        self.action_func = func

    def click(self) -> None:
        self.pressed = True
        self.image = self.images[self.pressed]
        self.call()

    def leave(self) -> None:
        self.pressed = False
        self.image = self.images[self.pressed]

    def is_pressed(self) -> bool:
        return self.pressed

    def collide(self, pos: (int, int)) -> bool:
        return self.rect.collidepoint(pos)

    def call(self):
        self.action_func()


class KeyAction(Sprite):
    def __init__(self, widget, coord: (int, int), current_image, not_current_image, *group, action=lambda: ...):
        super().__init__(*group)

        self.widget = widget

        self.images = {True: load_data.load_image(current_image),
                       False: load_data.load_image(not_current_image)
                       }
        self.current = False
        self.image = self.images[self.current]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord
        self.action_func = action

    def set_status(self, current: bool):
        self.current = current
        self.image = self.images[self.current]

    def set_action(self, func: object) -> None:
        self.action_func = func

    def set_coord(self, new_coord: (int, int)) -> None:
        self.rect.x, self.rect.y = new_coord

    def call(self):
        self.action_func()