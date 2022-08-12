import math
import cmath
from fileman import Fileman
import player
class Camera():
    def __init__(self, location, player_location=(0, 0), camera_type="follow_strict"):
        # free parameters
        self.fileman = Fileman()
        self.location = location
        self.player_location = player_location
        self.camera_type = camera_type

        # follow_in_circle parameters
        self.allowed_radius = 150  # what radius from camera_location is player allowed to move

        # follow_in_square parameters
        self.height = 200  # what height from camera_location up or down is player allowed to move
        self.width = 200  # what width from camera_location left or right is player allowed to move

    @staticmethod
    def round_location(location):
        return (round(location[0]), round(location[1]))

    def update(self, universe):

        ##############################EXPERIMENTAL FILEMAN#######################################################
        self.fileman.scene_writer("defSave.dsave", "camera_location_x=", "camera_location_x=" + " " + str(self.location[0]))
        self.fileman.scene_writer("defSave.dsave", "camera_location_x=", "camera_location_x=" + " " + str(self.location[1]))
        self.fileman.scene_writer("defSave.dsave", "camera_type=", "camera_type=" + " " + self.camera_type)
        self.fileman.scene_writer("defSave.dsave", "camera_self_allowed_radius=", "camera_self_allowed_radius=" + " " + str(self.allowed_radius))
        self.fileman.scene_writer("defSave.dsave", "camera_height=", "camera_height=" + " " + str(self.height))
        self.fileman.scene_writer("defSave.dsave", "camera_width=", "camera_width=" + " " + str(self.width))
        #########################################################################################################
        if self.camera_type == "follow_strict":
            self.player_location = universe.player.location
            self.adjust_camera_strict()
        elif self.camera_type == "follow_in_circle":
            self.player_location = universe.player.location
            self.adjust_camera_in_circle()
        elif self.camera_type == "follow_in_square":
            self.player_location = universe.player.location
            self.adjust_camera_in_square()

    def adjust_camera_strict(self):
        if self.location != self.player_location:
            self.location = self.player_location

    def adjust_camera_in_circle(self):
        displacement_x = self.player_location[0] - self.location[0]
        displacement_y = self.player_location[1] - self.location[1]
        if self.allowed_radius <= math.sqrt((displacement_x)**2 + (displacement_y)**2):
            angle = cmath.phase(complex(displacement_x, displacement_y))
            pos_x = self.allowed_radius * math.cos(angle)
            pos_y = self.allowed_radius * math.sin(angle)
            self.location = self.round_location((self.player_location[0] - pos_x, self.player_location[1] - pos_y))

    def adjust_camera_in_square(self):
        displacement_x = self.player_location[0] - self.location[0]
        displacement_y = self.player_location[1] - self.location[1]
        if abs(displacement_x) > self.width:
            print("SIDE")
            direction = displacement_x / abs(displacement_x)  # if negative player moves to the left else to the right
            self.location = self.round_location((self.player_location[0] - direction * self.width, self.location[1]))
        if abs(displacement_y) > self.height:
            print("HEIGHT")
            direction = displacement_y / abs(displacement_y)  # if negative player moves to up else to down
            self.location = self.round_location((self.location[0], self.player_location[1] - direction * self.height))
