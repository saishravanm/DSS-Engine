import pygame


class Mouse:
    def __init__(self):
        self.location = (0, 0)
        self.preview_color = (0, 255, 0)
        self.preview_radius = 10
        self.preview_thikness = 1

    def setup(self, coords_converter):
        self.location = coords_converter.to_universe(pygame.mouse.get_pos())
