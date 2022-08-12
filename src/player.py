import cmath
import math

# EXPERIMENTAL
import genericObject
from fileman import Fileman
NORM_K = (1 / math.sqrt(2))
FOV = math.pi / 3
HALF_FOV = FOV/2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
save = False;

class Player:
    def __init__(self):
        self.fileman = Fileman()
        self.state = "standing"
        self.location = (0, 0)
        self.speed = 5
        self.sprint = 10
        self.walk = 5
        self.crouch_speed = 2.5
        self.walk_speed = 5
        self.sprint_speed = 10
        self.run_multiplayer = 2
        self.crouch_multiplayer = 0.5
        self.walk_multiplayer = 1
        self.multiplayer = 1
        self.crouch_on = 0
        self.crouch_off = 1
        self.run_on = 2
        self.run_off = 1
        self.velocity = 0
        self.gravity_acceleration = 0.5
        self.jump_force = 15
        self.crouch = 1
        self.direction_h = 0
        self.direction_y = 0
        self.run = 1
        self.hit_box = (100, -100)
        self.stand_hit_box = (100, -200)
        self.crouch_hit_box = (100, -100)
        self.direction = (0, 0)
        self.rotation = (0, 0)
        self.current_speed = 0
        self.angle = 0
        self.player_angle = math.pi
        self.FOV = FOV
        self.HALF_FOV = HALF_FOV
        self.CASTED_RAYS = CASTED_RAYS
        self.STEP_ANGLE = STEP_ANGLE

        # EXPERIMENTAL
        self.rigid_body = genericObject.Player(self.location, self.angle)

    def move_normalize(self):
        speed_x = round(math.cos(self.angle) * self.current_speed)
        speed_y = round(math.sin(self.angle) * self.current_speed)
        self.location = (self.location[0] + speed_x, self.location[1] + speed_y)

    def update_speed(self):
        return self.speed * self.run

    def update_angle(self):
        return cmath.phase(complex(self.direction[0], self.direction[1]) * complex(self.rotation[0], self.rotation[1]))

    def move_h(self):
        self.location = (self.location[0] + self.direction_h * self.speed * self.run * self.crouch, self.location[1])

    def move_v(self):
        self.location = (self.location[0], self.location[1] + self.direction_y * self.speed * self.run * self.crouch)

    def setup(self, mouse_location):
        self.direction = (0, 0)
        self.current_speed = 0
        self.rotation = (mouse_location[0] - self.location[0], mouse_location[1] - self.location[1])
        self.angle = cmath.phase(complex(self.rotation[0], self.rotation[1]))

    def update(self):
        # ===================EXPERIMENTAL===================
        self.location = self.rigid_body.get_pos()
        # ==================================================

        ################################FILEMAN TEST##################################################



        self.fileman.scene_writer("defSave.dsave", "player_state=", "player_state=" + " " + self.state)
        self.fileman.scene_writer("defSave.dsave", "player_location_x=",
                                      "player_location_x=" + " " + str(self.location[0]))
        self.fileman.scene_writer("defSave.dsave", "player_location_y=",
                                      "player_location_y=" + " " + str(self.location[1]))
        self.fileman.scene_writer("defSave.dsave", "player_speed=", "player_speed=" + " " + str(self.speed))
        self.fileman.scene_writer("defSave.dsave", "player_sprint=", "player_sprint=" + " " + str(self.sprint))
        self.fileman.scene_writer("defSave.dsave", "player_walk=", "player_walk=" + " " + str(self.walk))
        self.fileman.scene_writer("defSave.dsave", "player_crouch_speed=",
                                      "player_crouch_speed=" + " " + str(self.crouch_speed))
        self.fileman.scene_writer("defSave.dsave", "player_walk_speed=",
                                      "player_walk_speed=" + " " + str(self.walk_speed))
        self.fileman.scene_writer("defSave.dsave", "player_sprint_speed=",
                                      "player_sprint_speed=" + " " + str(self.sprint_speed))
        self.fileman.scene_writer("defSave.dsave", "player_run_multiplayer=",
                                      "player_run_multiplayer=" + " " + str(self.run_multiplayer))
        self.fileman.scene_writer("defSave.dsave", "player_crouch_multiplayer=",
                                      "player_crouch_multiplayer=" + " " + str(self.crouch_multiplayer))
        self.fileman.scene_writer("defSave.dsave", "player_walk_multiplayer=",
                                      "player_walk_multiplayer=" + " " + str(self.walk_multiplayer))
        self.fileman.scene_writer("defSave.dsave", "player_crouch_on=",
                                      "player_crouch_on=" + " " + str(self.crouch_on))
        self.fileman.scene_writer("defSave.dsave", "player_crouch_off=",
                                      "player_crouch_off=" + " " + str(self.crouch_off))
        self.fileman.scene_writer("defSave.dsave", "player_run_on=", "player_run_on=" + " " + str(self.run_on))
        self.fileman.scene_writer("defSave.dsave", "player_run_off=", "player_run_off=" + " " + str(self.run_off))
        self.fileman.scene_writer("defSave.dsave", "player_velocity=",
                                      "player_velocity=" + " " + str(self.velocity))
        self.fileman.scene_writer("defSave.dsave", "player_gravity_acceleration=",
                                      "player_gravity_acceleration=" + " " + str(self.gravity_acceleration))
        self.fileman.scene_writer("defSave.dsave", "player_direction_h=",
                                      "player_direction_h=" + " " + str(self.direction_h))
        self.fileman.scene_writer("defSave.dsave", "player_direction_y=",
                                      "player_direction_y=" + " " + str(self.direction_y))
        self.fileman.scene_writer("defSave.dsave", "player_run=", "player_run=" + " " + str(self.run))
        self.fileman.scene_writer("defSave.dsave", "player_direction=",
                                      "player_direction=" + " " + str(self.direction))
        self.fileman.scene_writer("defSave.dsave", "player_rotation=",
                                      "player_rotation=" + " " + str(self.rotation))
        self.fileman.scene_writer("defSave.dsave", "player_angle=", "player_angle=" + " " + str(self.angle))
        self.fileman.scene_writer("defSave.dsave", "player_player_angle=",
                                      "player_player_angle=" + " " + str(self.player_angle))

        ######################################################################################################
        if self.direction != (0, 0):
            self.angle = self.update_angle()
            self.current_speed = self.update_speed()
            self.move_normalize()
            # ===================EXPERIMENTAL===================
            self.rigid_body.set_pos(self.location)
            # ==================================================
