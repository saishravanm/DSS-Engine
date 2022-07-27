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


# def draw_static(static_objects):
#     for static_object in static_objects:
#         static_object.draw(static_object.get_pos(), screen)
#
#
# def draw_kinetic(kinetic_objects):
#     for kinetic_object in kinetic_objects:
#         kinetic_object.draw(kinetic_object.get_pos(), screen)
#
#
# def draw_collidable_kinetic(collidable_kinetic_objects):
#     for collidable_kinetic_object in collidable_kinetic_objects:
#         collidable_kinetic_object.draw(collidable_kinetic_object.get_pos(), screen)
#
#
# def update_kinetic_object(list_of_objects):
#     for some_object in list_of_objects:
#         some_object.update()
#
#
# def update_collidable_kinetic_object(list_of_objects, tiles):
#     for some_object in list_of_objects:
#         some_object.update(tiles)


def update(tiles, render_obj):
    for level_object in tiles:
        level_object.update(tiles, render_obj.coords, render_obj.screen)


# static_list = [genericObject.Static((250,250))]
# kinetic_list = [genericObject.Kinetic((1, 0), 2, (50,50))]
# collidable_kinetic_list = [genericObject.CollidableKinetic((-1, 1), 2, (350, 50))]

map_list = [genericObject.Static((250,250)), genericObject.Kinetic((1, 0), 2, (50,50)), genericObject.CollidableKinetic((-1, 1), 2, (350, 50))]  # contains all the objects in them map

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
    # update_kinetic_object(kinetic_list)
    # update_collidable_kinetic_object(collidable_kinetic_list, static_list)
    update(map_list, render)

    # draw #
    # draw_static(static_list)
    # draw_kinetic(kinetic_list)
    # draw_collidable_kinetic(collidable_kinetic_list)

    # update display #
    pygame.display.update()
    mainClock.tick(60)