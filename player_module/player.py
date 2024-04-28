from pygame.sprite import Sprite, Group, spritecollideany
import load_data
from const import WIDTH, HEIGHT, Key
from player_module.moving_vector import PlayerMovingVector
from player_module.player_image_controller import PlayerImageController


class PlayerShadowSprite(Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_data.load_image('shadow.png')
        self.rect = self.image.get_rect()

    def update_coord(self, player_rect):
        self.rect.x = player_rect.x
        self.rect.y = player_rect.y + player_rect.height // 3 * 2

    def move_x(self, dx: int) -> None:
        self.rect.x += dx

    def move_y(self, dy: int) -> None:
        self.rect.y += dy


class PlayerSprite(Sprite):
    def __init__(self, scene, *group) -> None:
        super().__init__(*group)
        self.scene = scene
        self.images = PlayerImageController()
        self.image = self.images.main_image

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = HEIGHT // 2 - self.rect.height // 2
        self.game_position = [0, 0]

    def move_x(self, dx: int) -> None:
        self.game_position[0] += dx
        self.rect.x += dx

    def move_y(self, dy: int) -> None:
        self.game_position[1] += dy
        self.rect.y += dy

    def set_position(self, game_position: list[int, int] | tuple[int, int]) -> None:
        self.game_position: list = game_position

    def update_image(self, mv: PlayerMovingVector):
        if mv.x == 0 and mv.y == 0:
            image = self.images.update_image(self.images.STAY)
        else:
            image = self.images.update_image(self.images.RUNNING, mv.x, mv.y)
        self.image = image


class Player:
    """Фасад. Инкапсулирует в себе спрайт игрока, его тень (объект контроля движения), управление игроком."""
    def __init__(self, scene):
        self.scene = scene
        self.sprite_group = Group()
        self.player_sprite = PlayerSprite(scene, self.sprite_group)
        self.shadow_sprite = PlayerShadowSprite(self.sprite_group)
        self.shadow_sprite.update_coord(self.player_sprite.rect)

        self.moving_vector = PlayerMovingVector()

    def set_position(self, game_position: list[int, int] | tuple[int, int]) -> None:
        self.player_sprite.set_position(game_position)

    def update(self, barriers: Group) -> None:
        self.moving_vector.update()
        self.move(barriers)
        self.player_sprite.update_image(self.moving_vector)

    def move(self, barriers: Group) -> None:
        dx = self.moving_vector.x
        self.shadow_sprite.move_x(dx)
        if not spritecollideany(self.shadow_sprite, barriers):
            self.player_sprite.move_x(dx)
        self.shadow_sprite.move_x(-dx)

        dy = self.moving_vector.y
        self.shadow_sprite.move_y(dy)
        if not spritecollideany(self.shadow_sprite, barriers):
            self.player_sprite.move_y(dy)
        self.shadow_sprite.move_y(-dy)

    def keydown(self, key: Key) -> None:
        self.moving_vector.keydown(key)

    def keyup(self, key: Key) -> None:
        self.moving_vector.keyup(key)

    def draw(self, screen):
        self.sprite_group.draw(screen)
