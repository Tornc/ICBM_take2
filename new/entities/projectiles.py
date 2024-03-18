from abc import abstractmethod
import math
import random
import pygame
import const
import utils
import entities.sfx as sfx


class Projectile(pygame.sprite.Sprite):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__()

        self.attributes()

        if not active:
            return

        self.world = world
        self.initial_pos = initial_pos
        self.traveled_distance: float = 0
        self.angle = initial_angle + random.randint(-self.inaccuracy, self.inaccuracy)
        self.team = team

        if self.texture:
            self.set_original_img()
            self.set_img_rect()

    @abstractmethod
    def attributes(self):
        self.cooldown: int = 0
        self.damage: float = 0
        self.inaccuracy: int = 0
        self.range: float = 0
        self.size: int = 0
        self.speed: float = 0
        self.texture: const.Projectile = None

    def set_original_img(self):
        self.original_image = utils.scale_image(
            self.texture, desired_x=self.size
        )

    def set_img_rect(self):
        self.image = pygame.transform.rotate(
            self.original_image.copy(),
            -self.angle,
        )
        self.rect = self.image.get_rect(center=self.initial_pos)

    def update_pos_with_angle(self):
        # TODO: Weird speed-up issue when turning hard
        angle_in_radians = math.radians(self.angle)
        self.rect.centerx += round(self.speed * math.cos(angle_in_radians))
        self.rect.centery += round(self.speed * math.sin(angle_in_radians))

    def hit(self):
        self.kill()

    def check_out_of_range(self):
        if self.range:
            distance = math.hypot(
                self.old_pos[0] - self.rect.centerx,
                self.old_pos[1] - self.rect.centery,
            )

            self.traveled_distance += distance
            if self.traveled_distance > self.range:
                self.kill()

    def check_out_of_bounds(self):
        if (
            self.rect.x + self.rect.width < 0
            or self.rect.x > const.SCREEN_WIDTH
            or self.rect.y + self.rect.height < 0
            or self.rect.y > const.SCREEN_HEIGHT
        ):
            self.kill()

    def update(self):
        self.old_pos = self.rect.center
        self.update_pos_with_angle()
        self.check_out_of_range()
        self.check_out_of_bounds()


class Bullet(Projectile):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__(world, active, initial_pos, initial_angle, team)

    def attributes(self):
        self.cooldown: int = 100
        self.damage: float = 0.25
        self.inaccuracy: int = 10
        self.range: float = 750
        self.size: int = 20
        self.speed: float = 25
        self.texture: const.Projectile = const.Projectile.BULLET


class BulletHeavy(Projectile):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__(world, active, initial_pos, initial_angle, team)

    def attributes(self):
        self.cooldown = 750
        self.damage = 10
        self.inaccuracy = 0
        self.range = None
        self.size = 64
        self.speed = 10
        self.texture = const.Projectile.BULLET_HEAVY

    def hit(self):
        pass


class BulletCluster(Projectile):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__(world, active, initial_pos, initial_angle, team)

    def attributes(self):
        self.cooldown: int = 1500
        self.damage: float = 0
        self.inaccuracy: int = 0
        self.range: float = 750
        self.size: int = 64
        self.speed: float = 5
        self.texture: const.Projectile = const.Projectile.BULLET_FRAGMENTATION

        # Different from parent
        self.bomblet_amount: int = 12
        self.bomblet_range: float = 250
        self.bomblet_frag_amount: int = 12

    def hit(self):
        super().hit()
        angle_increment = 360 / self.bomblet_amount
        for i in range(self.bomblet_amount):
            b = BulletFragmentation(
                world=self.world,
                active=True,
                initial_pos=self.rect.center,
                initial_angle=i * angle_increment,
                team=self.team,
            )
            b.range = self.bomblet_range
            b.frag_amount = self.bomblet_frag_amount
            self.world.spawn_projectile(b)


class BulletFragmentation(Projectile):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__(world, active, initial_pos, initial_angle, team)

    def attributes(self):
        self.cooldown: int = 350
        self.damage: float = 0
        self.inaccuracy: int = 0
        self.range: float = 500
        self.size: int = 32
        self.speed: float = 10
        self.texture: const.Projectile = const.Projectile.BULLET_FRAGMENTATION

        # Different from parent
        self.frag_amount: int = 16

    def kill(self):
        super().kill()

        angle_increment = 360 / self.frag_amount
        for i in range(self.frag_amount):
            b = Fragment(
                world=self.world,
                active=True,
                initial_pos=self.rect.center,
                initial_angle=i * angle_increment,
                team=self.team,
            )
            self.world.spawn_projectile(b)


class Fragment(Projectile):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__(world, active, initial_pos, initial_angle, team)

    def attributes(self):
        self.cooldown: int = 50
        self.damage: float = 0.25
        self.inaccuracy: int = 15
        self.range: float = 200
        self.size: int = 5
        self.speed: float = 15
        self.texture: const.Projectile = const.Projectile.FRAGMENT


class MissileHoming(Projectile):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__(world, active, initial_pos, initial_angle, team)

    def attributes(self):
        self.cooldown: int = 500
        self.damage: float = 1
        self.inaccuracy: int = 0
        self.range: float = 1750
        self.size: int = 64
        self.speed: float = 7.5
        self.texture: const.Projectile = const.Projectile.MISSILE_HOMING

        # Different from parent
        self.turn_rate: float = 1.5

    def adjust_angle(self):
        target_angle = utils.angle_between_points(
            self.rect.center, pygame.mouse.get_pos()
        )
        angle_difference = ((target_angle - self.angle) + 180) % 360 - 180

        if angle_difference > 0:
            turn_amount = min(self.turn_rate, angle_difference)
        elif angle_difference < 0:
            turn_amount = -min(self.turn_rate, abs(angle_difference))
        else:
            turn_amount = 0

        self.angle = (self.angle + turn_amount) % 360

    def update_img_rect(self):
        self.image = pygame.transform.rotate(
            self.original_image.copy(),
            -self.angle,
        )
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.range:
            travel_proportion = self.traveled_distance / self.range
            max_darkness = 0.75
            darkness_value = int(255 * max_darkness * travel_proportion)
            self.image.set_alpha(255 - darkness_value)

    def update(self):
        super().update()

        self.adjust_angle()
        self.update_img_rect()


class MissileNuke(MissileHoming):
    def __init__(
        self,
        world=None,
        active: bool = False,
        initial_pos: tuple[int, int] = (0, 0),
        initial_angle: float = 0,
        team: const.Team = None,
    ):
        super().__init__(world, active, initial_pos, initial_angle, team)

    def attributes(self):
        self.cooldown: int = 5000
        self.damage: float = 1
        self.inaccuracy: int = 0
        self.range: float = None
        self.size: int = 128
        self.speed: float = 2.5
        self.texture: const.Projectile = const.Projectile.MISSILE_NUKE

        # Different from parent
        self.turn_rate: float = 0.2
        self.explosion_size: int = 750

    def hit(self):
        super().hit()
        self.world.spawn_projectile(
            ExplosionProjectile(
                world=self.world,
                initial_pos=self.rect.center,
                size=self.explosion_size,
                team=self.team,
            )
        )


class ExplosionProjectile(sfx.Explosion):
    def __init__(
        self,
        world=None,
        initial_pos: tuple[int, int] = (0, 0),
        size: int = 32,
        team: const.Team = None,
    ):
        super().__init__(initial_pos, size)
        self.world = world
        self.initial_pos = initial_pos
        self.team = team

        self.attributes()

    def attributes(self):
        self.damage = 1

    def hit(self):
        pass


class Laser:
    def __init__():
        pass
