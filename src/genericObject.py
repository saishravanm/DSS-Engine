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

        self.velocity = Vector2D(0.0, 0.0)
        self.angular_velocity = 0.0

        self.torque = 0.0
        self.forces = Vector2D(0.0, 0.0)

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

    def update(self, dt):
        pass


class Static(GenericObject):
    def __init__(self, pos, angle=0, shape=sh.Rect(100, 100)):
        super(Static, self).__init__(pos, angle, shape)


class Kinetic(GenericObject):
    def __init__(self, pos, angle=0, shape=sh.Rect(100, 100)):
        super(Kinetic, self).__init__(pos, angle, shape)

    def add_world_force(self, force, offset):

        if self.shape.offset_in_object(offset):
            self.forces += force
            self.torque += offset.cross(force.rotate(self.angle))

    def add_torque(self, torque):
        self.torque += torque

    def reset(self):
        self.forces = Vector2D(0.0, 0.0)
        self.torque = 0.0

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

    def __init__(self, pos, angle=0, shape=sh.Rect(100, 100)):
        super(CollidableKinetic, self).__init__(pos, angle, shape)


class Spinner(GenericObject):
    def __init__(self, pos, angle=0, shape=sh.Rect(100, 100)):
        super(Spinner, self).__init__(pos, angle, shape)
        self.angular_velocity = 90

    def update(self, dt):
        self.angle += self.angular_velocity * dt


class Player(GenericObject):
    def __int__(self, pos, angle=0, shape=sh.Rect(100, 100)):
        super(Player, self).__init__(pos, angle, shape)

    def get_pos(self):
        return (self.pos.x, self.pos.y)

    def set_pos(self, pos):
        self.pos = Vector2D(pos[0], pos[1])

    def set_angle(self, angle):
        self.angle = angle

    def update(self, dt):
        pass
