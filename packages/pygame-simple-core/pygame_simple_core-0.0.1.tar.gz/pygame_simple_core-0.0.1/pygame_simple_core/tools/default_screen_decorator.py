import pygame as pg


def default_screen(function):
    def wrapper(self, screen=None):
        if screen == None:
            screen = pg.display.get_surface()

        function(self, screen)

    return wrapper
