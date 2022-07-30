

class Shape():
    def __init__(self, shape_type):
        self.shape_type = shape_type


class Rect(Shape):
    def __init__(self, width, height, mass=None, restitution=0.5):
        super(Rect, self).__init__("rect")
        self.width = width
        self.height = height

        if mass is None:
            mass = width * height
        self.mass = mass
        self.restitution = restitution
        self.inertia = mass * (width ** 2 + height ** 2) / 12

        self.vertices = (
            (-self.width / 2, -self.height / 2),
            (self.width / 2, -self.height / 2),
            (self.width / 2, self.height / 2),
            (-self.width / 2, self.height / 2)
        )

        self.edges = (
            (self.width, 0),
            (0, self.height),
            (-self.width, 0),
            (0, -self.height),
        )

        # self.sprite = pygame.Surface((width, height))
        # self.sprite.set_colorkey((0, 0, 0))
        # self.sprite.fill((0, 0, 0))
        # pygame.draw.rect(self.sprite, (255, 255, 255), (0, 0, width - 2, height - 2), 2)

    def offset_in_object(self, offset):
        return abs(offset[0]) <= self.width / 2 and abs(offset[1]) <= self.height / 2


class Circle(Shape):
    def __init__(self, radius, mass=None, restitution=0.5):
        super(Circle, self).__init__("circle")
        self.radius = radius
