import time
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

    def add(self, *bodies):
        self.bodies += bodies
        for body in bodies:
            print("Body added", id(body))

    def remove(self, body):
        self.bodies.remove(body)
        print("Body removed", id(body))

    def update(self, dt):
        start = time.time()
        tested = []

        def timer(name):
            def watch(f):
                start = time.time()
                try:
                    return f()
                finally:
                    end = time.time()
                    watch.spent = end - start
            watch.spent = 0
            watch.print = lambda: print("%s time: %s" % (name, watch.spent))
            return watch

        t0 = 0
        t1 = timer("Experimental")
        t2 = timer("Normalize")
        t3 = timer("Collision")
        t4 = timer("Other Collision")
        t5 = timer("Intersection")

        for body in self.bodies:

            for other_body in self.bodies:
                if other_body not in tested and other_body is not body and (body.shape.mass != inf or other_body.shape.mass != inf):  # objects with inf mass don't collide with other inf mass objects
                    start1 = time.time()
                    collision, depth, normal = body.collide(other_body)
                    end1 = time.time()
                    #print("SAT time: ", end1 - start1)
                    t0 += end1 - start1
                    if t0 > 0.005:
                        break 

                    if collision:

                        # EXPERIMENTAL
                        def timed1():
                            body.react(other_body)
                            other_body.react(body)
                        t1(timed1)
                        # ============

                        normal = t2(lambda: normal.normalize())

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

                        start1 = time.time()
                        body_collision_edge = t3(lambda: body.get_collision_edge(-direction))
                        other_body_collision_edge = t4(lambda: other_body.get_collision_edge(direction))
                        end1 = time.time()
                        #print("Find edges time: ", end1 - start1)

                        contact_point = t5(lambda: line_intersection(body_collision_edge, other_body_collision_edge))

                        if contact_point:
                            radius = (body.pos - contact_point)
                            body.angular_velocity = body.angular_velocity + (radius.dot(j * normal / body.shape.inertia))

                            radius = (other_body.pos - contact_point)
                            other_body.angular_velocity = other_body.angular_velocity - (
                                radius.dot(j * normal / other_body.shape.inertia))

            if t0 > 0.005:
                break

            tested.append(body)
            body.update(dt)
        end = time.time()

        t1.print()
        t2.print()
        t3.print()
        t4.print()
        t5.print()
        print ("Total time: ", end - start)
