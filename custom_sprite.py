from pygame.sprite import Sprite


class CustomSprite(Sprite):
    def is_collided_with(self, sprite: Sprite) -> bool:
        return self.rect.colliderect(sprite.rect)

    def sort_key(self) -> int:
        return self.rect.bottom

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

