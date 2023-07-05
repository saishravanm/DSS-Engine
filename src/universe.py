from player import Player
from mouse import Mouse

# EXPERIMENTAL
import genericObject
from physics import PhysicsWorld
from math import inf


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

        # EXPERIMENTAL
        self.physics = PhysicsWorld()
        self.dt = 1/60
        #self.physics.add(self.player.rigid_body)
        self.physics.player = self.player.rigid_body
        #self.physics.add(
        #    genericObject.Static((500,500), 0),
        #    genericObject.Static((700, 500), 0, genericObject.sh.Rect(50, 50, inf)),
        #    genericObject.Spinner((700, 700), 0),
        #    genericObject.Spinner((800, 700), 0, genericObject.sh.Rect(150, 10, inf)),
        #    genericObject.Spinner((950, 700), 0, genericObject.sh.Rect(150, 10, inf)),
        #    genericObject.TouchMe((500,100), 0, genericObject.sh.Rect(100, 100, inf))
        #)
        self.physics.add_groups(
            genericObject.Group((100, 100), 0, genericObject.sh.Rect(200, 200, inf),
                genericObject.Static((100, 100), 0),
                genericObject.Static((50, 50), 0, genericObject.sh.Rect(50, 50, inf))
            )
        )

    def update(self):  # does something every frame, could be useful for enemy AI or update some values
        if self.mode == "game":
            self.player.update()
            # ===================EXPERIMENTAL===================
            self.physics.update(self.dt)
            # ==================================================
        pass

    def setup(self, coords_converter):
        if self.mode == "game":
            self.mouse.setup(coords_converter)
            self.player.setup(self.mouse.location)
        pass
