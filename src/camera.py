

class Camera():
    def __init__(self, location,player_location, camera_type):
        self.location = location
        self.player_location = player_location
        self.camera_type = camera_type

    def update(self, universe):
        if self.camera_type == "follow_strict":
            self.player_location = universe.player.location
            self.adjust_camera_strict()

    def adjust_camera_strict(self):
        if self.location != self.player_location:
            self.location = self.player_location
