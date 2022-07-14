import cmath
import math

# EXPERIMENTAL
import genericObject

NORM_K = (1 / math.sqrt(2))
FOV = math.pi / 3
HALF_FOV = FOV/2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
class Player:
    def __init__(self):
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
        if self.direction != (0, 0):
            self.angle = self.update_angle()
            self.current_speed = self.update_speed()
            self.move_normalize()
            # ===================EXPERIMENTAL===================
            self.rigid_body.set_pos(self.location)
            # ==================================================
