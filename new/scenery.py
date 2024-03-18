import pygame
import utils
import const


class Background(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = utils.scale_image(
            image_path, desired_x=const.SCREEN_WIDTH
        )
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(
            (const.SCREEN_WIDTH, int(const.SCREEN_HEIGHT * 0.05))
        )
        self.image.fill((36, 28, 28))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, const.SCREEN_HEIGHT - self.rect.height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
