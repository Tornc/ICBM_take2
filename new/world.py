import copy
import pygame
import random

import const
import entities.buildings as buildings
import entities.enemies as enemies
import entities.projectiles as projectiles
import scenery


class World:
    def __init__(self):
        self.__ground_group_single: pygame.sprite.Group = pygame.sprite.GroupSingle()
        self.__city_group: pygame.sprite.Group = pygame.sprite.Group()
        self.__turret_group: pygame.sprite.Group = pygame.sprite.Group()
        self.__projectile_group: pygame.sprite.Group = pygame.sprite.Group()
        self.__enemy_group: pygame.sprite.Group = pygame.sprite.Group()
        self.__sfx_group: pygame.sprite.Group = pygame.sprite.Group()

        self.__score: int = 0
        self.__money: int = 0

        self.__max_health = 3
        self.__current_health = self.__max_health

        self.__starting_difficulty = 1
        self.__current_difficulty = self.__starting_difficulty
        self.__difficulty_multiplier = 1.05
        self.__difficulty_increase_interval = 100

        self.__enemy_timer = pygame.USEREVENT + 1
        self.__enemy_base_spawn_rate = 1000
        self.__enemy_current_spawn_rate = self.__enemy_base_spawn_rate
        pygame.time.set_timer(self.__enemy_timer, self.__enemy_base_spawn_rate)

        self.__enemy_types = [enemies.Asteroid, enemies.AsteroidMega, enemies.UFO]
        self.__enemy_weigths = [80, 15, 5]

        self.__spawn_ground()

        self.__test_init()

    def __test_init(self):
        self.__enemy_base_spawn_rate = 1000

        enemy = enemies.UFO(self)
        enemy.rect.centerx = const.SCREEN_WIDTH / 2
        # enemy.current_health = 10000
        self.spawn_enemy(enemy)

        current_x = 0
        building_amount = 25
        for i in range(1, building_amount):
            current_x = i * (const.SCREEN_WIDTH / building_amount)
            if current_x >= const.SCREEN_WIDTH:
                break

            self.__city_group.add(
                buildings.CityBuilding(
                    self,
                    (
                        current_x,
                        self.__ground_group_single.sprite.rect.y,
                    ),
                )
            )
        amnt = 4  # actual amnt = amnt - 1
        projs = [projectiles.BulletFragmentation, projectiles.MissileNuke, projectiles.BulletFragmentation]
        for i in range(1, amnt):
            self.spawn_turret(
                buildings.Turret(
                    self,
                    (
                        int(const.SCREEN_WIDTH * (1 / amnt) * i),
                        self.__ground_group_single.sprite.rect.y,
                    ),
                    projs[i - 1](),
                )
            )

    def __test_update(self):
        pass

    def event_loop(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == self.__enemy_timer:
                self.__spawn_random_enemy()
            if pygame.mouse.get_pressed()[0]:
                for turret in self.__turret_group:
                    turret.shoot()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    self.__money -= 100

    def __handle_collisions(self):
        self.__handle_ground_enemies_collision()
        self.__handle_city_enemies_collision()
        self.__handle_turrets_enemies_collision()
        self.__handle_projectiles_enemies_collision()

    def update(self):
        # TODO: use deltatime for all movement/rotation/animation
        # needs: position var, so can't use rect.center for position
        # since that's in ints: position -> round(position) = rect.center
        self.__handle_collisions()

        self.__ground_group_single.update()
        self.__city_group.update()
        self.__turret_group.update()
        self.__projectile_group.update()
        self.__enemy_group.update()
        self.__sfx_group.update()

        self.__update_difficulty()

        self.__test_update()

    def draw(self, screen):
        self.__ground_group_single.draw(screen)
        self.__city_group.draw(screen)
        self.__projectile_group.draw(screen)
        self.__turret_group.draw(screen)
        self.__enemy_group.draw(screen)
        self.__sfx_group.draw(screen)

    def __handle_ground_enemies_collision(self):
        enemy = pygame.sprite.spritecollideany(
            self.__ground_group_single.sprite, self.__enemy_group
        )
        if enemy:
            enemy.hit()
            self.__current_health -= enemy.damage

    def __handle_city_enemies_collision(self):
        for city_building in self.__city_group:
            enemy = pygame.sprite.spritecollideany(city_building, self.__enemy_group)
            if enemy:
                city_building.hit(enemy.damage)
                enemy.hit()

    def __handle_turrets_enemies_collision(self):
        for turret in self.__turret_group:
            enemy = pygame.sprite.spritecollideany(turret, self.__enemy_group)
            if enemy:
                turret.hit(enemy.damage)
                enemy.hit()

    def __handle_projectiles_enemies_collision(self):
        for projectile in self.__projectile_group:
            enemy = pygame.sprite.spritecollideany(projectile, self.__enemy_group)
            if enemy:
                projectile.hit()
                enemy.hit(projectile.damage)
                if not enemy.alive():
                    self.__score += enemy.score
                    self.__money += enemy.score

    def __update_difficulty(self):
        interval = self.__difficulty_increase_interval
        score = self.__score

        start = self.__starting_difficulty
        mulp = self.__difficulty_multiplier
        self.__current_difficulty = start * mulp ** (score // interval)

        base = self.__enemy_base_spawn_rate
        cur_dif = self.__current_difficulty
        spawn_rate = int(base * (1.0 / cur_dif))
        if self.__enemy_current_spawn_rate != spawn_rate:
            self.__enemy_current_spawn_rate = spawn_rate
            pygame.time.set_timer(self.__enemy_timer, spawn_rate)

    def spawn_projectile(self, projectile):
        self.__projectile_group.add(projectile)

    def spawn_sfx(self, sfx):
        self.__sfx_group.add(sfx)

    def spawn_enemy(self, enemy):
        self.__enemy_group.add(enemy)

    def spawn_turret(self, turret: buildings.Turret):
        self.__turret_group.add(turret)

    def __spawn_random_enemy(self):
        enemy = random.choices(self.__enemy_types, self.__enemy_weigths)[0](self)
        enemy.rect.center = (
            random.randint(
                0 + enemy.image.get_width(),
                const.SCREEN_WIDTH - enemy.image.get_width(),
            ),
            -100,
        )
        self.__enemy_group.add(enemy)

    def __spawn_ground(self):
        self.__ground_group_single.add(scenery.Ground())

    def get_score(self):
        return self.__score

    def get_money(self):
        return self.__money

    def get_current_health(self):
        return self.__current_health

    def get_max_health(self):
        return self.__max_health

    def get_current_difficulty(self):
        return self.__current_difficulty

    def get_difficulty_multiplier(self):
        return self.__difficulty_multiplier

    def get_turret_group(self):
        return self.__turret_group

    def get_enemy_group(self):
        return self.__enemy_group
