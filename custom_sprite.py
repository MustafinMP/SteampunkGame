from pygame.sprite import Sprite


class CustomSprite(Sprite):
    def draw(self, screen):
        screen.blit(self.image, self.rect)