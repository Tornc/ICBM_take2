from enum import Enum, StrEnum

# CONSTANTS
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
LOCKED_FPS = 60
PATH_PIXEL_FONT = "assets\\font\\Pixeltype.ttf"
PATH_BACKGROUND = "assets\\textures\\sky_2.png"
PATH_SKYLINE = "assets\\textures\\skyline.png"

PATH_EXPLOSION = "assets\\textures\\explosion\\exp"


class Team(Enum):
    PLAYER = 1
    ENEMY = 2


class Projectile(StrEnum):
    BULLET = "assets\\textures\\projectiles\\bullet.png"
    BULLET_HEAVY = "assets\\textures\\projectiles\\bulletHeavy.png"
    BULLET_FRAGMENTATION = "assets\\textures\\projectiles\\bulletFragmentation.png"
    FRAGMENT = "assets\\textures\\projectiles\\fragment.png"
    MISSILE_HOMING = "assets\\textures\\projectiles\\missile_small.png"
    MISSILE_NUKE = "assets\\textures\\projectiles\\nuke.png"


class Enemy(StrEnum):
    ASTEROID = "assets\\textures\enemy\\asteroid"
    UFO = "assets\\textures\\enemy\\ufo.png"


class Turret(StrEnum):
    TURRET_BASE = "assets\\textures\\building\\turret\\turret_base.png"
    TURRET_BARREL = "assets\\textures\\building\\turret\\bullet_barrel.png"


class City(StrEnum):
    CITY_B1 = "assets\\textures\\building\\city\\b1.png"
    CITY_B2 = "assets\\textures\\building\\city\\b2.png"
    CITY_B3 = "assets\\textures\\building\\city\\b3.png"
    CITY_B4 = "assets\\textures\\building\\city\\b4.png"
