import math

NORM_K = (1 / math.sqrt(2))


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
        self.direction = 0
        self.direction_h = 0
        self.direction_y = 0
        self.run = 1
        self.hit_box = (100,-200)
        self.stand_hit_box = (100, -200)
        self.crouch_hit_box = (100, -100)

    def move_normalize(self):  # TODO under development.
        if self.direction_h * self.direction_y == 0:  # normalize if needed
            self.location = (self.location[0] + self.direction_h * self.speed * self.run * self.crouch, self.location[1])
            self.location = (self.location[0], self.location[1] + self.direction_y * self.speed * self.run * self.crouch)
        else:
            self.location = (self.location[0] + self.direction_h * NORM_K * self.speed * self.run * self.crouch, self.location[1])
            self.location = (self.location[0], self.location[1] + self.direction_y * NORM_K * self.speed * self.run * self.crouch)

    def move_h(self):
        self.location = (self.location[0] + self.direction_h * self.speed * self.run * self.crouch, self.location[1])

    def move_v(self):
        self.location = (self.location[0], self.location[1] + self.direction_y * self.speed * self.run * self.crouch)
