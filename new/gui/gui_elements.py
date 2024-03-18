import math
import pygame

import const
import entities.buildings


class Text(pygame.sprite.Sprite):
    def __init__(
        self, text: str = "text", size: int = 32, position: tuple[int, int] = (100, 100)
    ):
        super().__init__()
        self.text = text
        self.size = size
        self.position = position

        self.font: pygame.font.Font = pygame.font.Font(const.PATH_PIXEL_FONT, self.size)
        self.update()
        self.rect: pygame.Rect = self.image.get_rect(midbottom=self.position)

    def update(self):
        self.image: pygame.Surface = self.font.render(self.text, False, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class HealthBar(pygame.sprite.Sprite):
    def __init__(
        self, current_health: float, max_health: float, health_bar_length: int
    ):
        super().__init__()
        self.current_health = current_health
        self.max_health = max_health
        self.health_bar_length = health_bar_length

        self.health_ratio: float = self.max_health / self.health_bar_length

        self.update()

    def set_image_rect(self):
        self.image: pygame.Surface = pygame.Surface((self.health_bar_length, 25))
        self.image.fill((255, 255, 255))
        self.image.fill(
            (255, 0, 0), (0, 0, self.current_health / self.health_ratio, 25)
        )
        self.rect: pygame.Rect = self.image.get_rect(topleft=(10, 25))

    def update(self):
        self.set_image_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Reticle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect()

        pygame.draw.circle(self.image, pygame.Color("white"), (15, 15), 15, 2)
        pygame.draw.circle(self.image, pygame.Color("red"), (15, 15), 2)

    def update(self):
        self.rect.center: tuple[int, int] = pygame.mouse.get_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class AimLine(pygame.sprite.Sprite):
    """
    TODO: extremely laggy in large numbers >7 due to large rect
    + filling it with 0, 0, 0 every update
    """

    def __init__(self, turret: entities.buildings.Turret):
        super().__init__()
        self.turret = turret

        self.position: tuple[int, int] = self.turret.position
        self.range: int = self.turret.projectile.range
        self.set_image_rect()

    def set_image_rect(self):
        self.image: pygame.Surface = pygame.Surface(
            (const.SCREEN_WIDTH, const.SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self.rect: pygame.Rect = self.image.get_rect()

    def draw_line(self):
        mouse_pos = pygame.mouse.get_pos()
        green = (0, 255, 0, 128)

        if self.range:
            angle = math.degrees(
                math.atan2(
                    mouse_pos[1] - self.position[1], mouse_pos[0] - self.position[0]
                )
            )
            angle_radians = math.radians(angle)

            out_of_range_x = int(
                self.position[0] + self.range * math.cos(angle_radians)
            )
            out_of_range_y = int(
                self.position[1] + self.range * math.sin(angle_radians)
            )
            out_of_range_pos = (out_of_range_x, out_of_range_y)

            dist_out_of_range_pos = math.dist(self.position, out_of_range_pos)
            dist_mouse_pos = math.dist(self.position, mouse_pos)

            red = (255, 0, 0, 255)

            end_pos = (
                mouse_pos
                if dist_mouse_pos < dist_out_of_range_pos
                else out_of_range_pos
            )

            if dist_mouse_pos >= dist_out_of_range_pos:
                pygame.draw.line(self.image, red, end_pos, mouse_pos)
        else:
            end_pos = mouse_pos

        pygame.draw.line(self.image, green, self.position, end_pos)

    def update(self):
        if not self.turret.alive():
            self.kill()
            return

        self.image.fill((0, 0, 0, 0))
        self.draw_line()


def draw_reticle(screen):
    mouse_pos = pygame.mouse.get_pos()
    white = (255, 255, 255)
    red = (255, 0, 0)
    pygame.draw.circle(screen, white, mouse_pos, 15, 2)
    pygame.draw.circle(screen, red, mouse_pos, 2)

def draw_aim_line(screen, turret, mouse_pos):
    start_pos = turret.position
    range = turret.range
    reloading = turret.reloading
    cooldown = turret.cooldown

    if range:
        angle = math.degrees(
            math.atan2(mouse_pos[1] - start_pos[1], mouse_pos[0] - start_pos[0])
        )
        angle_radians = math.radians(angle)

        out_of_range_x = int(start_pos[0] + range * math.cos(angle_radians))
        out_of_range_y = int(start_pos[1] + range * math.sin(angle_radians))
        out_of_range_pos = (out_of_range_x, out_of_range_y)

        dist_out_of_range_pos = math.dist(start_pos, out_of_range_pos)
        dist_mouse_pos = math.dist(start_pos, mouse_pos)

        red = (191, 0, 0)

        end_pos = (
            mouse_pos if dist_mouse_pos < dist_out_of_range_pos else out_of_range_pos
        )

        if dist_mouse_pos >= dist_out_of_range_pos:
            pygame.draw.line(screen, red, end_pos, mouse_pos)
    else:
        end_pos = mouse_pos

    if cooldown <= 300 or not reloading:
        green = (0, 191, 0)
        pygame.draw.line(screen, green, start_pos, end_pos)
    else:
        grey = (128, 128, 128)
        pygame.draw.line(screen, grey, start_pos, end_pos)
