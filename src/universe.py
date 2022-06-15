from player import Player
from mouse import Mouse


class Universe:
    def __init__(self):
        self.surface_altitudes = [((100,100),(500,100))]
        self.collision_points = []
        self.player = Player()
        self.mouse = Mouse()
        self.mode = "map"
        self.buildMode = "line"
        self.mouse_coords = (0,0)
        self.pointPressed = (-1,-1)
        self.pointZero = (-1,-1)
        self.pointLeft = (-1,-1)
        self.gravity = -5

    def update(self):  # does something every frame, could be useful for enemy AI or update some values
        if self.mode == "game":
            self.player.update()
        pass

    def setup(self, coords_converter):
        if self.mode == "game":
            self.mouse.setup(coords_converter)
            self.player.setup(self.mouse.location)
        pass
