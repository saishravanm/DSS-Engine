from vectors import Vector2D
from math import copysign, inf


# from https://stackoverflow.com/a/20677983
def line_intersection(line1, line2):  # maybe get rid of Vector2D component
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return Vector2D(x, y)


class PhysicsWorld:
    def __init__(self):
        self.bodies = []
        self.groups = []
        self.objs = []
        self.player = None

    def add_groups(self, *groups):
        self.groups += groups
        for group in groups:
            print("Group added", id(group))

    def add(self, *bodies):
        self.bodies += bodies
        for body in bodies:
            print("Body added", id(body))

    def remove(self, body):
        self.bodies.remove(body)
        print("Body removed", id(body))

    def update(self, dt):
        tested = []
        test_groups = []

        for group in self.groups:
            collision, depth, normal = group.collide(self.player)
            if collision:
                test_groups.append(group)

        print(len(test_groups))
        other_body = self.player

        for group in test_groups:
            for body in group.bodies:
                if other_body not in tested and other_body is not body and (body.shape.mass != inf or other_body.shape.mass != inf):  # objects with inf mass don't collide with other inf mass objects
                    collision, depth, normal = body.collide(other_body)

                    if collision:

                        # EXPERIMENTAL
                        body.react(other_body)
                        other_body.react(body)
                        # ============

                        normal = normal.normalize()

                        rel_vel = (body.velocity - other_body.velocity)
                        j = -(1 + body.shape.restitution) * rel_vel.dot(normal) / normal.dot(
                            normal * (1 / body.shape.mass + 1 / other_body.shape.mass))

                        direction = body.pos - other_body.pos
                        magnitude = normal.dot(direction)

                        if body.shape.mass != inf:
                            body.pos += normal * depth * copysign(1, magnitude)
                        if other_body.shape.mass != inf:
                            other_body.pos -= normal * depth * copysign(1, magnitude)

                        body.velocity = body.velocity + j / body.shape.mass * normal
                        other_body.velocity = other_body.velocity - j / other_body.shape.mass * normal

                        body_collision_edge = body.get_collision_edge(-direction)
                        other_body_collision_edge = other_body.get_collision_edge(direction)
                        contact_point = line_intersection(body_collision_edge, other_body_collision_edge)

                        if contact_point:
                            radius = (body.pos - contact_point)
                            body.angular_velocity = body.angular_velocity + (radius.dot(j * normal / body.shape.inertia))

                            radius = (other_body.pos - contact_point)
                            other_body.angular_velocity = other_body.angular_velocity - (
                                radius.dot(j * normal / other_body.shape.inertia))

            tested.append(body)
            body.update(dt)
