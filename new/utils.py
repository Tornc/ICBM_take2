import math
import pygame


def scale_image(image_path, desired_x=None, desired_y=None):
    original_image = pygame.image.load(image_path).convert_alpha()
    if desired_x is None and desired_y is None:
        return original_image

    original_width, original_height = original_image.get_size()

    if desired_x is not None:
        scaling_factor_x = desired_x / original_width
    if desired_y is not None:
        scaling_factor_y = desired_y / original_height

    if desired_x is None:
        scaling_factor_x = scaling_factor_y
    if desired_y is None:
        scaling_factor_y = scaling_factor_x

    scaled_width = int(original_width * scaling_factor_x)
    scaled_height = int(original_height * scaling_factor_y)

    return pygame.transform.scale(original_image, (scaled_width, scaled_height))


def angle_between_points(point_1, point_2):
    return math.degrees(math.atan2(point_2[1] - point_1[1], point_2[0] - point_1[0]))
