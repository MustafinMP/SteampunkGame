import pygame
import load_data


class AbstractButton(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def is_pressed(self):
        pass


class AbstractActionButton(pygame.sprite.Sprite):
    def __init__(self, x, y, pressed_image, not_pressed_image, *group):
        super().__init__(*group)
        self.images = {True: load_data.load_image(pressed_image),
                       False: load_data.load_image(not_pressed_image)
                       }
        self.pressed = False
        self.image = self.images[self.pressed]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def event_update(self, game, event):
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.pressed = True
                    self.image = self.images[self.pressed]
            case pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.pressed = False
                    self.image = self.images[self.pressed]

    def is_pressed(self):
        return self.pressed


