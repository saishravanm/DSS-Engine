import shape as sh
import renderParams as rp


class GenericObject():
    def __init__(self, pos, shape=sh.Rect(100, 100)):
        self.pos = pos
        self.shape = shape  # type of shape square or circle
        self.render_params_map = {"rect":rp.Rect, "circle":rp.Circle}
        self.render_params = self.render_params_map[self.shape.shape_type]

    def get_shape(self):
        return self.shape

    def get_pos(self):
        return self.pos


class Static(GenericObject):
    def __init__(self, pos, shape=sh.Rect(100, 100)):
        super(Static, self).__init__(pos, shape)

    def update(self, tiles, converter, screen):
        pass

# class CollidableStatic(Static):
#     def __init__(self, pos, shape):
#         self.pos = pos
#         self.shape = shape


# class NonCollidableStatic(Static):
#     def __init__(self, pos, shape):
#         self.pos = pos
#         self.shape = shape


class Kinetic(GenericObject):
    def __init__(self, direction, speed, pos, shape=sh.Rect(100, 100)):
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


class CollidableKinetic(Kinetic):
    def __init__(self, direction, speed, pos, shape=sh.Rect(100, 100)):
        super(CollidableKinetic, self).__init__(direction, speed, pos, shape)
        self.collision_map = {"Static":True}
        # self.collision_check_map = {"rec": self.rec_collision_checker}

    def update(self, tiles, converter, screen):
        if self.direction != (0, 0):
            pass


# class NonCollidableKinetic(Kinetic):
#     def __init__(self, pos, shape, direction, speed):
#         self.pos = pos
#         self.ppos = self.pos  # previous position
#         self.cpos = self.pos  # current position
#         self.fpos = self.pos  # future position
#         self.shape = shape
#         self.direction = direction
#         self.speed = speed
