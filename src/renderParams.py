

class RenderParams():
    def __init__(self, params_type, color=(250, 250, 250)):
        self.params_type = params_type
        self.color = color

        self.colorkey = (0, 0, 0)
        self.fill = (0, 0, 0)


class Rect(RenderParams):
    def __init__(self, thickness=0, curve=0):
        super(Rect, self).__init__("rect")
        self.thickness = thickness  # Thickness of the line, to fill make it 0
        self.curve = curve  # Makes corners of rect curved to make it normal make it 0


class Circle(RenderParams):
    def __init__(self, thickness=0):
        super(Circle, self).__init__("circle")
        self.thickness = thickness  # Thickness of the line, to fill make it 0
        self.draw_top_right = True  # To use later
        self.draw_top_left = True  # To use later
        self.draw_bottom_right = True  # To use later
        self.draw_bottom_left = True  # To use later
