import pygame


class Mouse:
    def __init__(self):
        self.location = (0, 0)

    def setup(self, coords_converter):
        self.location = coords_converter.to_universe(pygame.mouse.get_pos())
