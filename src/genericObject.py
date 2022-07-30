import shape as sh
import renderParams as rp
import sys

from vectors import Vector2D


class GenericObject():
    def __init__(self, pos, angle=0, shape=sh.Rect(100, 100)):
        self.pos = Vector2D(pos[0], pos[1])  # Be careful to not change it back to tuple
        self.angle = angle
        self._shape = shape  # type of shape square or circle
        self.render_params_map = {"rect":rp.Rect, "circle":rp.Circle}
        self._render_params = self.render_params_map[self._shape.shape_type]()

    @property
    def shape(self):
        return self._shape

    @property
    def render_params(self):
        return self._render_params

    @property
    def vertices(self):
        return [
            self.pos + Vector2D(v).rotate(-self.angle) for v in self.shape.vertices
        ]

    @property
    def edges(self):
        return [
            Vector2D(v).rotate(self.angle) for v in self.shape.edges
        ]

    def get_pos(self):
        return self.pos

    def collide(self, other):
        # Exit early for optimization
        if (self.pos - other.pos).length() > max(self.shape.width, self.shape.height) + max(other.shape.width, other.shape.height):  # TODO change second part after ">"
            return False, None, None

        def project(vertices, axis):
            dots = [vertex.dot(axis) for vertex in vertices]
            return Vector2D(min(dots), max(dots))

        collision_depth = sys.maxsize
        collision_normal = None

        for edge in self.edges + other.edges:
            axis = Vector2D(edge).orthogonal().normalize()
            projection_1 = project(self.vertices, axis)
            projection_2 = project(other.vertices, axis)
            min_intersection = max(min(projection_1), min(projection_2))
            max_intersection = min(max(projection_1), max(projection_2))
            overlapping = min_intersection <= max_intersection
            if not overlapping:
                return False, None, None
            else:
                overlap = max_intersection - min_intersection
                if overlap < collision_depth:
                    collision_depth = overlap
                    collision_normal = axis
        return True, collision_depth, collision_normal

    def get_collision_edge(self, normal):
        max_projection = -sys.maxsize
        support_point = None
        vertices = self.vertices
        length = len(vertices)

        for i, vertex in enumerate(vertices):
            projection = vertex.dot(normal)
            if projection > max_projection:
                max_projection = projection
                support_point = vertex
                if i == 0:
                    right_vertex = vertices[-1]
                else:
                    right_vertex = vertices[i - 1]
                if i == length - 1:
                    left_vertex = vertices[0]
                else:
                    left_vertex = vertices[i + 1]

        if right_vertex.dot(normal) > left_vertex.dot(normal):  # TODO fix references
            return (right_vertex, support_point)
        else:
            return (support_point, left_vertex)


class Static(GenericObject):
    def __init__(self, pos, angle=0, shape=sh.Rect(100, 100)):
        super(Static, self).__init__(pos, angle, shape)

    def update(self, tiles):
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
    def __init__(self, pos, speed, speed_delta, angle=0, shape=sh.Rect(100, 100)):
        super(Kinetic, self).__init__(pos, angle, shape)
        self.speed_delta = speed_delta
        self.speed = speed
        self.color = (250, 0, 0)
        self.speed_xy = self.get_speed_xy()

        self.velocity = Vector2D(0.0, 0.0)
        self.angular_velocity = 0.0

        self.torque = 0.0
        self.forces = Vector2D(0.0, 0.0)

    def get_direction(self):
        return self.speed_delta

    def get_speed(self):
        return self.speed

    def get_speed_xy(self):
        ratio = abs(self.speed_delta[0]) + abs(self.speed_delta[1])
        ratio_speed = (self.speed / ratio)
        speed_x = ratio_speed * self.speed_delta[0]
        speed_y = ratio_speed * self.speed_delta[1]
        return (speed_x, speed_y)

    def add_world_force(self, force, offset):

        if self.shape.offset_in_object(offset):
            self.forces += force
            self.torque += offset.cross(force.rotate(self.angle))

    def add_torque(self, torque):
        self.torque += torque

    def reset(self):
        self.forces = Vector2D(0.0, 0.0)
        self.torque = 0.0

    def move(self):
        self.pos = Vector2D(self.pos[0] + self.speed_xy[0], self.pos[1] + self.speed_xy[1])

    # def update(self, tiles):  # junk
    #     if self.speed_delta != (0, 0):
    #         self.move()

    def update(self, dt):
        acceleration = self.forces / self.shape.mass
        self.velocity += acceleration * dt
        self.pos += self.velocity * dt

        angular_acceleration = self.torque / self.shape.inertia
        self.angular_velocity += angular_acceleration * dt
        self.angle += self.angular_velocity * dt

        self.reset()


class CollidableKinetic(Kinetic):

    collision_map = {Static}

    def __init__(self, pos, speed, speed_delta, angle=0, shape=sh.Rect(100, 100)):
        super(CollidableKinetic, self).__init__(pos, speed, speed_delta, angle, shape)

    # def update(self, tiles):
    #     if self.speed_delta != (0, 0):
    #         self.move()


# class NonCollidableKinetic(Kinetic):
#     def __init__(self, pos, shape, direction, speed):
#         self.pos = pos
#         self.ppos = self.pos  # previous position
#         self.cpos = self.pos  # current position
#         self.fpos = self.pos  # future position
#         self.shape = shape
#         self.direction = direction
#         self.speed = speed
