from pygame.sprite import Sprite


class CustomSprite(Sprite):
    def is_collided_with(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)