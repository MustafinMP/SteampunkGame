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


class AbstractButton(Sprite):
    def __init__(self, coord: (int, int), image, *group):
        super().__init__(*group)
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord

    def collide(self, pos: (int, int)) -> bool:
        return self.rect.collidepoint(pos)


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

    def click(self):
        self.pressed = True
        self.image = self.images[self.pressed]
        self.call()

    def leave(self):
        self.pressed = False
        self.image = self.images[self.pressed]

    def is_pressed(self):
        return self.pressed

    def collide(self, pos: (int, int)) -> bool:
        return self.rect.collidepoint(pos)

    def set_coord(self, new_coord: (int, int)):
        self.rect.x, self.rect.y = new_coord

    def call(self):
        pass


