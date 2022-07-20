

class Shape():
    def __init__(self, shape_type):
        self.shape_type = shape_type


class Rect(Shape):
    def __init__(self, width, height):
        super(Rect, self).__init__("rect")
        self.width = width
        self.height = height


class Circle(Shape):
    def __init__(self, radius):
        super(Circle, self).__init__("circle")
        self.radius = radius
