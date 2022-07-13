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
        self.thickness = 0
        self.curve = 0
        self.draw_map = {"rec":self.draw_rec}
        self.define_hit_box_map = {"rec":self.define_rec()}
        self.look = self.define_hit_box_map[self.shape]  # is it rectangle hit-box or circle hit-box

    def get_shape(self):
        return self.shape

    def get_pos(self):
        return self.pos

    def define_rec(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    # def draw(self, screen_pos, screen):
    #     self.draw_map[self.shape](screen_pos, screen)
    #
    # def draw_rec(self, screen_pos, screen):
    #     pygame.draw.rect(screen, self.color, (screen_pos[0], screen_pos[1], self.width, self.height), self.thickness, self.curve)

    def draw(self, converter, screen):
        self.draw_map[self.shape](converter, screen)

    def draw_rec(self, converter, screen):
        screen_pos = converter.from_universe(self.pos)
        pygame.draw.rect(screen, self.color, (screen_pos[0], screen_pos[1], self.width, self.height), self.thickness, self.curve)


class Static(GenericObject):
    def __init__(self, pos, shape="rec"):
        super(Static, self).__init__(pos, shape)

    def update(self, tiles, converter, screen):
        self.draw(converter, screen)

# class CollidableStatic(Static):
#     def __init__(self, pos, shape):
#         self.pos = pos
#         self.shape = shape


# class NonCollidableStatic(Static):
#     def __init__(self, pos, shape):
#         self.pos = pos
#         self.shape = shape


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

    def update(self, tiles, converter, screen):  # junk
        self.move()
        self.draw(converter, screen)


class CollidableKinetic(Kinetic):
    def __init__(self, direction, speed, pos, shape="rec"):
        super(CollidableKinetic, self).__init__(direction, speed, pos, shape)
        self.collision_map = {"Static":True}
        # self.collision_check_map = {"rec": self.rec_collision_checker}

    def collision_test(self, rect, tiles):
        collisions = []
        for tile in tiles:
            if tile != self and rect.colliderect(tile.look):
                if self.collision_map[type(tile).__name__]:
                    collisions.append(tile)
        return collisions

    def collision_checker(self, rect, movement, tiles):
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

    def update(self, tiles, converter, screen):
        # new_look = self.collision_check_map[self.shape](self.look, self.speed_xy, tiles)
        if self.direction != (0, 0):
            new_look = self.collision_checker(self.look, self.direction, tiles)
            self.pos = (new_look.x, new_look.y)
        self.draw(converter, screen)


# class NonCollidableKinetic(Kinetic):
#     def __init__(self, pos, shape, direction, speed):
#         self.pos = pos
#         self.ppos = self.pos  # previous position
#         self.cpos = self.pos  # current position
#         self.fpos = self.pos  # future position
#         self.shape = shape
#         self.direction = direction
#         self.speed = speed
