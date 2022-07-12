import pygame
import math
import cmath


class GenericObject():
    def __init__(self, pos, shape="rec"):
        self.pos = pos
        self.shape = shape  # type of shape square or circle
        self.color = (0, 250, 0)
        self.width = 100
        self.height = 100
        self.thickness = 5
        self.curve = 0
        self.draw_map = {"rec":self.draw_rec}
        self.define_map = {"rec":self.define_rec()}
        self.look = self.define_map[self.shape]  # is it rectangle hit-box or circle hit-box

    def get_shape(self):
        return self.shape

    def get_pos(self):
        return self.pos

    def define_rec(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def draw(self, screen_pos, screen):
        self.draw_map[self.shape](screen_pos, screen)

    def draw_rec(self, screen_pos, screen):
        pygame.draw.rect(screen, self.color, (screen_pos[0], screen_pos[1], self.width, self.height), self.thickness, self.curve)


class Static(GenericObject):
    def __init__(self, pos, shape="rec"):
        super(Static, self).__init__(pos, shape)


# class CollidableStatic(Static):
#     def __init__(self, pos, shape):
#         self.pos = pos
#         self.shape = shape
#
#
# class NonCollidableStatic(Static):
#     def __init__(self, pos, shape):
#         self.pos = pos
#         self.shape = shape
#
#
class Kinetic(GenericObject):
    def __init__(self, direction, speed, pos, shape="rec"):
        super(Kinetic, self).__init__(pos, shape)
        self.direction = direction
        self.speed = speed
        self.color = (250, 0, 0)
        self.speed_xy = self.get_speed_xy()

    def get_direction(self):
        return self.direction

    def get_speed(self):
        return self.speed

    def get_speed_xy(self):
        ratio = abs(self.direction[0]) + abs(self.direction[1])
        ratio_speed = (self.speed / ratio)
        speed_x = ratio_speed * self.direction[0]
        speed_y = ratio_speed * self.direction[1]
        return (speed_x, speed_y)

    def move(self):
        # ratio = self.direction[0] + self.direction[1]
        # ratio_speed = (self.speed / ratio)
        # speed_x = ratio_speed * self.direction[0]
        # speed_y = ratio_speed * self.direction[1]
        self.pos = (self.pos[0] + self.speed_xy[0], self.pos[1] + self.speed_xy[1])

    def update(self):
        self.move()


class CollidableKinetic(Kinetic):
    def __init__(self, direction, speed, pos, shape="rec"):
        super(CollidableKinetic, self).__init__(direction, speed, pos, shape)
        self.collision_map = {"Static":True}
        self.collision_check_map = {"rec": self.get_next_rect}

    def collision_test(self, rect, tiles):
        collisions = []
        for tile in tiles:
            if rect.colliderect(tile.look):
                if self.collision_map[type(tile).__name__]:
                    collisions.append(tile)
        return collisions

    def get_next_rect(self, rect, movement, tiles):
        rect.x += movement[0]
        collisions = self.collision_test(rect, tiles)
        for tile in collisions:
            if movement[0] > 0:
                rect.right = tile.look.left
            if movement[0] < 0:
                rect.left = tile.look.right
        rect.y += movement[1]
        collisions = self.collision_test(rect, tiles)
        for tile in collisions:
            if movement[1] > 0:
                rect.bottom = tile.look.top
            if movement[1] < 0:
                rect.top = tile.look.bottom
        return rect

    def update(self, tiles):
        new_look = self.collision_check_map[self.shape](self.look, self.speed_xy, tiles)
        self.pos = (new_look.x, new_look.y)
        print("doing some magic")


# class NonCollidableKinetic(Kinetic):
#     def __init__(self, pos, shape, direction, speed):
#         self.pos = pos
#         self.ppos = self.pos  # previous position
#         self.cpos = self.pos  # current position
#         self.fpos = self.pos  # future position
#         self.shape = shape
#         self.direction = direction
#         self.speed = speed
