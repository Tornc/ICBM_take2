import random
import pygame

import const
import utils


class Building(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # TODO: rewrite turret and citybuilding

    def set_darkness(self):
        if self.current_health < self.max_health:
            health_proportion = 1 - (self.current_health / self.max_health)
            darkness_value = int(255 * 0.75 * health_proportion)
            self.image.set_alpha(255 - darkness_value)

    def hit(self, impact_damage=9999999):
        self.current_health -= impact_damage
        if self.current_health <= 0:
            self.kill()


class Turret(Building):
    def __init__(self, world, position: tuple[int, int], projectile):
        super().__init__()

        self.world = world
        self.position = position
        self.projectile = projectile
        self.last_shot = pygame.time.get_ticks()
        self.cooldown: int = self.projectile.cooldown
        self.range: int = self.projectile.range
        self.angle: float = 0

        self.set_attributes()
        self.set_original_img()
        self.set_img_rect()

    def set_attributes(self):
        self.max_health: float = 3.0
        self.current_health: float = self.max_health
        self.size: int = 100

    def set_original_img(self):
        self.position = (self.position[0], self.position[1] - self.size * 0.5)
        self.original_base_image = utils.scale_image(
            const.Turret.TURRET_BASE, desired_x=self.size
        )
        self.original_barrel_image = utils.scale_image(
            const.Turret.TURRET_BARREL, desired_x=self.size
        )

    def set_img_rect(self):
        self.base_image = self.original_base_image.copy()
        self.barrel_image = pygame.transform.rotate(
            self.original_barrel_image.copy(),
            -self.angle,
        )

        base_rect = self.base_image.get_rect(
            center=((self.size * 0.5, self.size * 0.75))
        )
        barrel_rect = self.barrel_image.get_rect(center=(base_rect.midtop))

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.image.blit(self.base_image, base_rect)
        self.image.blit(self.barrel_image, barrel_rect)
        dark_grey = (128, 128, 128)
        pygame.draw.circle(self.image, (dark_grey), base_rect.midtop, 20)
        self.rect = self.image.get_rect(center=(self.position))

        self.set_darkness()

    def shoot(self):
        if not self.reloading:
            self.last_shot = pygame.time.get_ticks()

            new_projectile = type(self.projectile)(
                world=self.world,
                active=True,
                initial_pos=self.position,
                initial_angle=self.angle,
                team=const.Team.PLAYER,
            )
            self.world.spawn_projectile(new_projectile)

    def update(self):
        self.angle = utils.angle_between_points(self.position, pygame.mouse.get_pos())

        now = pygame.time.get_ticks()
        self.reloading = now - self.last_shot < self.cooldown

        self.set_img_rect()


class CityBuilding(Building):
    def __init__(self, world, position: tuple[int, int], base_health: float = 1.0):
        super().__init__()

        self.world = world
        self.position = position
        self.base_health = base_health

        self.set_img_rect()

    def set_img_rect(self):
        # TODO: buildings shouldn't spawn inside of turrets
        city_weights = [40, 40, 20, 20]
        city = random.choices(list(const.City), weights=city_weights)[0]
        index = list(const.City).index(city) + 1

        self.max_health = self.base_health * index
        self.current_health = self.max_health

        self.image = pygame.image.load(city).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, random.uniform(0.45, 0.56))
        self.rect = self.image.get_rect(midbottom=self.position)

    def hit(self, damage):
        super().hit(damage)
        self.set_darkness()
