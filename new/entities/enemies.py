import math
import random
import pygame
from abc import abstractmethod

import const
import utils
import entities.sfx as sfx
import entities.projectiles as projectiles


class Enemy(pygame.sprite.Sprite):
    def __init__(self, world):
        super().__init__()

        self.world = world

        self.attributes()
        self.last_impact = pygame.time.get_ticks()
        self.explosion_cooldown: int = 150
        self.max_health *= world.get_current_difficulty()
        self.current_health: float = self.max_health
        self.speed *= world.get_current_difficulty()
        self.set_img_rect()

    @abstractmethod
    def attributes(self):
        self.damage: float = 0
        self.max_health: float = 0.0
        self.score: int = 0
        self.size: int = 0
        self.speed: int = 0

    @abstractmethod
    def set_img_rect(self):
        raise NotImplementedError(
            f"Subclasses must implement {self.set_img_rect.__name__}."
        )

    def hit(self, damage: float = 9999999):
        self.current_health -= damage

        if self.current_health > 0:
            now = pygame.time.get_ticks()
            if now - self.last_impact >= self.explosion_cooldown:
                self.last_impact = now
                self.world.spawn_sfx(
                    sfx.Explosion(
                        self.rect.midbottom, self.size * random.uniform(0.1, 0.25)
                    )
                )
        else:
            self.kill()
            self.world.spawn_sfx(
                sfx.Explosion(self.rect.midbottom, self.size * random.uniform(1, 4))
            )

    def out_of_bounds_check(self):
        if (
            self.rect.x + self.rect.width < 0
            or self.rect.x > const.SCREEN_WIDTH
            # Enemies need to spawn in off-screen
            or self.rect.y + self.rect.height < 0 - 200
            or self.rect.y > const.SCREEN_HEIGHT
        ):
            self.kill()

    def update(self):
        self.out_of_bounds_check()


class UFO(Enemy):
    def __init__(self, world):
        super().__init__(world)

        self.time_last_direction_change = pygame.time.get_ticks()
        self.time_last_down_movement = pygame.time.get_ticks()
        self.time_last_shot = pygame.time.get_ticks()
        self.direction = random.choice([-1, 1])
        self.distance_traveled = 0

    def attributes(self):
        self.damage: float = 15
        self.max_health: float = 15
        self.score: int = 50
        self.size: int = 128
        self.speed: int = 2

    def set_img_rect(self):
        self.image = utils.scale_image(const.Enemy.UFO, desired_x=self.size)
        self.rect = self.image.get_rect()

    def hit(self, damage: float = 9999999):
        super().hit(damage)
        self.set_darkness()

    def set_darkness(self):
        if self.current_health < self.max_health:
            health_proportion = 1 - (self.current_health / self.max_health)
            darkness_value = int(255 * 0.75 * health_proportion)
            self.image.set_alpha(255 - darkness_value)

    def move(self):
        # MOVE SIDE TO SIDE
        if self.current_time - self.time_last_direction_change >= 5000:
            self.direction = random.choice([-1, 1])
            self.time_last_direction_change = self.current_time

        self.rect.x += self.speed * self.direction

        if self.rect.x <= 0 or self.rect.x + self.size >= const.SCREEN_WIDTH:
            self.direction *= -1

        # MOVE DOWN
        if self.distance_traveled < const.SCREEN_HEIGHT * 0.15:
            self.rect.y += self.speed
            self.distance_traveled += self.speed
        elif self.current_time - self.time_last_down_movement >= 15000:
            self.time_last_down_movement = self.current_time
            self.distance_traveled = 0

    def shoot(self):
        if self.current_time - self.time_last_shot < 3000:
            return
        self.time_last_shot = self.current_time

        target_positions: list[tuple[int, int]] = []
        for turret in self.world.get_turret_group():
            target_positions.append(turret.position)

        if not target_positions:
            angle = 270
        else:
            # given a list of target positions, find the one closest to us
            # (self.rect.center), and get the angle
            closest_target = min(
                target_positions, key=lambda pos: math.dist(self.rect.center, pos)
            )
            angle = utils.angle_between_points(self.rect.center, closest_target)

            # new_projectile = projectiles.BulletCluster(
            #     world=self.world,
            #     active=True,
            #     initial_pos=self.rect.center,
            #     initial_angle=angle,
            #     team=const.Team.ENEMY,
            # )
            # TODO: suitable projectile
            # self.world.spawn_enemy_projectile(new_projectile)

    def update(self):
        super().update()
        self.current_time = pygame.time.get_ticks()

        self.move()
        self.shoot()

# TODO: REWORK ALL PROJECTILES AND PROJECTILES:
# _actually_ use that team property! (or use 2 groups)
# Damage is based on health, lower hp = lower damage
# e.g. 10 hp meteorite gets hit with 6 dmg, it now deals 4 dmg.
# projectiles hitting each other? deal dmg to each other.
# hp = 0 -> dmg = 0
# BUT! there may be projectiles/enemies with 0 dmg, e.g. flares / shields(?)
class Asteroid(Enemy):
    def __init__(self, world):
        super().__init__(world)

    def attributes(self):
        self.damage: float = 1
        self.max_health: float = 0.5
        self.score: int = 1
        self.size: int = 32
        self.speed: int = 2

    def set_img_rect(self):
        self.images: list[pygame.Surface] = []

        for i in range(1, 3):
            img = utils.scale_image(f"{const.Enemy.ASTEROID}{i}.png", self.size)
            self.images.append(img)

        self.index: float = 0
        self.image: pygame.Surface = self.images[int(self.index)]
        self.rect: pygame.Rect = self.image.get_rect()

    def update_img(self):
        if self.index >= len(self.images):
            self.index = 0

        self.image = self.images[int(self.index)]
        self.index += 0.1

        if self.current_health < self.max_health:
            health_proportion = 1 - (self.current_health / self.max_health)
            max_darkness = 0.5
            darkness_value = int(255 * max_darkness * health_proportion)
            self.image.set_alpha(255 - darkness_value)

    def update(self):
        super().update()
        self.rect.y += self.speed

        self.update_img()


class AsteroidMega(Asteroid):
    def __init__(self, world):
        super().__init__(world)

    def attributes(self):
        self.damage: float = 10
        self.max_health: float = 10
        self.score: int = 10
        self.size: int = 128
        self.speed: int = 1
