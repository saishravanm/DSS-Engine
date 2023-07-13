from player import Player
from mouse import Mouse

# EXPERIMENTAL
import genericObject
from edit import Edit
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
        self.edit = Edit()
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
                genericObject.Static((100, 100), 0, genericObject.sh.Rect(100, 100, inf)),
                genericObject.Static((50, 50), 0, genericObject.sh.Rect(50, 50, inf))
            ),
            genericObject.Group((400, 200), 0, genericObject.sh.Rect(400, 400, inf),
                genericObject.Static((400, 200), 0, genericObject.sh.Rect(100, 100, inf)),
                genericObject.Static((250, 250), 0, genericObject.sh.Rect(50, 50, inf))
            )
        )

    def add_group(self):
        angle = 0
        mouse_pos = self.edit.get_mouse_pos(self.mouse.location)
        width = mouse_pos[0] - self.edit.start[0]
        height = mouse_pos[1] - self.edit.start[1]
        pos = (self.edit.start[0] + width/2, self.edit.start[1] + height/2)
        print("Group end is at pos: ", pos)
        self.physics.add_groups(genericObject.Group(pos, angle, genericObject.sh.Rect(width, height, inf)))

    def find_selected_group(self):
        print("creating box")
        group = self.physics.find_selected_group(
            genericObject.Static(
                (self.mouse.location[0], self.mouse.location[1]),
                0,
                genericObject.sh.Rect(1, 1, inf)
            )
        )

        if group:
            self.edit.main_group = group
            print(id(self.edit.main_group), type(self.edit.main_group))
        else:
            print("No group there")

    def add_bodie_to_group(self):
        angle = 0
        mouse_pos = self.edit.get_mouse_pos(self.mouse.location)
        width = mouse_pos[0] - self.edit.start[0]
        height = mouse_pos[1] - self.edit.start[1]
        pos = (self.edit.start[0] + width/2, self.edit.start[1] + height/2)
        print("Bodie end is at pos: ", pos)
        self.edit.main_group.add(genericObject.Static(pos, angle, genericObject.sh.Rect(width, height, inf)))

    def update(self):  # does something every frame, could be useful for enemy AI or update some values
        if self.mode == "game":
            self.player.update()
            # ===================EXPERIMENTAL===================
            self.physics.update(self.dt)
            # ==================================================
        pass

    def setup(self, coords_converter):
        self.mouse.setup(coords_converter)
        if self.mode == "game":
            #self.mouse.setup(coords_converter)
            self.player.setup(self.mouse.location)
        pass
