# setup #
import pygame, sys
import genericObject
from render import Renderer

# setup pygame/window #
mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Physics Explanation')
# screen = pygame.display.set_mode((1000, 1000), 0, 32)
display = (1000,1000)  # display
screen = pygame.display.set_mode(display)
scale = (1,1)

render = Renderer(screen, ((0,0), display), scale)

map_list = [genericObject.Static((250,250)), genericObject.Kinetic((50,50), 2, (1, 0)), genericObject.CollidableKinetic((350, 50), 2, (-1, 1))]  # contains all the objects in them map


def update_gen_obj(gen_obj_list):
    for gen_obj in gen_obj_list:  # WARNING!!! gen_obj_list contains gen_obj so don't do collision checker strait with gen_obj_list
        gen_obj.update(gen_obj_list)


# loop #
while True:

    # clear display #
    screen.fill((0, 0, 0))

    # event handling #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # update #
    update_gen_obj(map_list)

    # draw #
    render.draw_gen_obj(map_list)

    # update display #
    pygame.display.update()
    mainClock.tick(60)
