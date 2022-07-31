import random
import traceback
from math import inf

import pygame
from pygame.locals import *

import genericObject
import shape
from vectors import Vector2D
from physics import PhysicsWorld
from render import Renderer


pygame.display.init()
pygame.font.init()
pygame.display.set_caption("Simple physics example")
default_font = pygame.font.Font(None, 24)
screen_size = (1280, 768)
game_surface = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

scale = (1,1)
render = Renderer(game_surface, ((0,0), screen_size), scale)

world = PhysicsWorld()
world.add(
    genericObject.CollidableKinetic((350, 500), 0, shape.Rect(200, 100, inf)),
    genericObject.Kinetic((350, 300), 0, shape.Rect(200, 100, inf)),
    genericObject.Static((700, 500), 0, shape.Rect(200, 100, inf)),
    # genericObject.GenericObject((700, 300), 0, shape.Rect(200, 100, inf)),
    # genericObject.GenericObject((900, 600), 0, shape.Rect(50, 50, inf)),
    genericObject.Spinner((900, 200), 0, shape.Rect(50, 10, inf)),
    # genericObject.Static((900, 150), 0, shape.Rect(50, 50, inf))
)
screen_center = Vector2D(screen_size) / 2
mouse_pos = screen_center


def get_input():
    mouse_buttons = pygame.mouse.get_pressed()
    global mouse_pos
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            return False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return False
        elif event.type == pygame.MOUSEBUTTONUP and mouse_buttons[0]:
            body = genericObject.CollidableKinetic(
                (screen_center.x, screen_center.y),
                random.randint(0, 90),
                shape.Rect(50, 50, 10)
            )
            world.add(body)
            body.velocity = Vector2D(mouse_pos) - screen_center
    return True


def draw():
    game_surface.fill((40, 40, 40))

    for body in world.bodies:
        render.draw_gen_obj_rect_2(body)
    pygame.draw.line(game_surface, (0, 255, 0), screen_center, mouse_pos, 2)

    game_surface.blit(default_font.render('Objects: {}'.format(len(world.bodies)), True, (255, 255, 255)), (0, 0))
    game_surface.blit(default_font.render('FPS: {0:.0f}'.format(clock.get_fps()), True, (255, 255, 255)), (0, 24))
    pygame.display.update()


def main():
    dt = 1 / 60
    while True:
        if not get_input():
            break
        world.update(dt)
        for body in world.bodies:
            if body.pos.x < 0 or body.pos.x > screen_size[0] or \
                    body.pos.y < 0 or body.pos.y > screen_size[1]:
                world.remove(body)
        draw()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        pygame.quit()
        input()
