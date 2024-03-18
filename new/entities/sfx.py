import pygame

import utils
import const

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        # TODO: use a more low res explosion
        self.images = []
        for num in range(1, 6):
            img = utils.scale_image(
                f"{const.PATH_EXPLOSION}{num}.png", size
            )
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=position)

        self.explosion_sound = pygame.mixer.Sound("assets\\sounds\\explosion.wav")
        # TODO: factor in size as well
        self.explosion_sound.set_volume((position[1] / const.SCREEN_HEIGHT) + 0.15)
        self.explosion_sound.play()

    def update(self):
        if self.index >= len(self.images):
            self.kill()
            return

        self.image = self.images[int(self.index)]
        self.index += 0.15