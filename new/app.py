from enum import Enum
import random
import sys
import pygame

import world
import scenery
import gui.gui as gui
import const


class State(Enum):
    QUIT = -1
    MAIN_MENU = 0
    PLAY = 1
    SHOP = 2
    PAUSE = 3


class App(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        pygame.mouse.set_visible(False)

        self.background = scenery.Background(const.PATH_BACKGROUND)
        self.skyline_background = scenery.Background(const.PATH_SKYLINE)
        self.skyline_background.rect.centery = (
            const.SCREEN_HEIGHT - self.skyline_background.image.get_height() * 0.333
        )
        self.world = world.World()
        self.world_gui = gui.Gui(self.clock, self.world)

        # bg_music = pygame.mixer.Sound("assets\\sounds\\Mi_Mi_Mi.wav")
        # bg_music.set_volume(0.05)
        # bg_music.play(loops = -1)

        self.done = False
        self.state = State.PLAY

    def update(self):
        if self.state == State.PLAY:
            self.world.update()
            self.world_gui.update()
        elif self.state == State.SHOP:
            pass

    def draw(self):
        if self.state == State.PLAY:
            self.background.draw(self.screen)
            self.skyline_background.draw(self.screen)
            self.world.draw(self.screen)
            self.world_gui.draw(self.screen)
        elif self.state == State.SHOP:
            pass

        pygame.display.flip()

    def event_loop(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.state = State.QUIT
                return

        if self.state == State.PLAY:
            self.world.event_loop(self.events)
        elif self.state == State.SHOP:
            pass

    def main_loop(self):
        # TODO: ADD SHOP
        while self.state != State.QUIT:
            self.event_loop()
            self.update()
            self.draw()
            self.clock.tick(const.LOCKED_FPS)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
    pygame.display.set_caption("ICBM v2.1")
    App().main_loop()
    pygame.quit()
    sys.exit()
