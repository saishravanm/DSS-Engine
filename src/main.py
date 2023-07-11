import sys, pygame;
import initMethods
import drawMethods
import pygame
import settings

from action import DoneAction
from translator import Translator
from universe import Universe
from coords import CoordConverter
from render import Renderer
from pygame.locals import *


clock = pygame.time.Clock()
pygame.init()

# pygame.display.init()  # initialization of display
display = (1000,1000)  # display
screen = pygame.display.set_mode(display)
surface = pygame.Surface(display)

scale = (1,1)
moving = False
dragging = False

universe = Universe()
# coords = CoordConverter(scale, ((0,0), display))  # here you can scale and modify out put on the display
render = Renderer(screen, ((0,0), display), scale)


def main_loop():
    translator = Translator(settings.TRANSLATION_MAP, DoneAction())

    def collect_actions():
        result = translator.translate_pressed(universe.mode)
        for event in pygame.event.get():
            universe.mouseCoord = pygame.mouse.get_pos()
            result += translator.translate_event(universe.mode, event)
        return result

    while True:
        universe.setup(render.coords)

        actions = collect_actions()

        if any(action.is_done() for action in actions):
            break

        for action in actions:
            action.change_universe(universe, render)

        universe.update()

        render.update(universe)
        pygame.display.flip()

        clock.tick(settings.FPS)

if __name__ == "__main__":
    main_loop()
    pygame.quit()
