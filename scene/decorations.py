from pygame.sprite import Sprite, Group
from geometry_abstractions import Position
from const import RATIO
import load_data
import locations


class AbstractDecoration(Sprite):
    def __init__(self, position: Position, image: str, *group):
        super().__init__(*group)
        self.image = load_data.load_image(image)
        self.rect = self.image.get_rect()
        self.game_position: Position = position
        self.rect.x, self.rect.y = position.x, position.y


class Floor(AbstractDecoration):
    """Объект пола, не восприимчив к столкновениям"""


class Barrier(AbstractDecoration):
    """Объект любых препятствий, восприимчив к столкновениям"""


class RedirectZone(AbstractDecoration):
    """Особый объект пола, может сменять текущую локацию"""

    def __init__(self, position, image, redirect_address, redirect_image, *group):
        super().__init__(position, image, *group)
        self.redirect_address = redirect_address
        self.hint_group = Group()
        self.hint_key = Sprite(self.hint_group)
        self.hint_key.image = load_data.load_image(redirect_image)
        self.hint_key.rect = self.hint_key.image.get_rect()
        self.update_hint_coord()

    def update_hint_coord(self):
        self.hint_key.rect.x = self.rect.center[0] - 16
        self.hint_key.rect.y = self.rect.center[1] + 32

    def get_redirect_address(self):
        return self.redirect_address

    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw_hint(self, screen):
        self.update_hint_coord()
        self.hint_group.draw(screen)