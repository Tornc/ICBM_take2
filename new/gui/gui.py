import pygame
import world
import const
import gui.gui_elements as gui_elements


class Gui(object):
    def __init__(self, clock: pygame.time.Clock, world: world.World):
        self.__clock = clock
        self.__world = world

        self.__fps_counter = gui_elements.Text(size=32, position=(35, 25))
        self.__health_bar = gui_elements.HealthBar(
            self.__world.get_current_health(), self.__world.get_max_health(), 150
        )

        self.__score_board = gui_elements.Text(
            size=64, position=(const.SCREEN_WIDTH * 0.5, 100)
        )
        self.__money_counter = gui_elements.Text(size=32, position=(35, 75))

        # TEST
        self.__curdif = gui_elements.Text(
            size=32, position=(const.SCREEN_WIDTH * 0.9, 25)
        )

    def update(self):
        self.__fps_counter.text = f"FPS: {int(self.__clock.get_fps())}"
        self.__fps_counter.update()

        self.__health_bar.current_health = self.__world.get_current_health()
        self.__health_bar.update()

        self.__score_board.text = f"{self.__world.get_score()}"
        self.__score_board.update()

        self.__money_counter.text = f"${self.__world.get_money()}"
        self.__money_counter.update()

        self.__curdif.text = f"Difficulty: {self.__world.get_current_difficulty()}"
        self.__curdif.update()

    def draw(self, screen):
        for turret in self.__world.get_turret_group():
            gui_elements.draw_aim_line(screen, turret, pygame.mouse.get_pos())

        gui_elements.draw_reticle(screen)

        self.__fps_counter.draw(screen)
        self.__health_bar.draw(screen)
        self.__score_board.draw(screen)
        self.__money_counter.draw(screen)

        self.__curdif.draw(screen)
