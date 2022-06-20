import pygame

from coords import CoordConverter
from camera import Camera


class Renderer:

    def __init__(self, screen, viewport, scale):
        self.coords = CoordConverter(scale, viewport)
        self.camera = Camera(self.coords.to_universe((viewport[1][0]/2, viewport[1][1]/2)), (0, 0), "follow_strict")
        self.screen = screen
        self.viewport = viewport
        self.scale = scale
        self.speed = 5
        self.color = (250,0,0)  # (250,250,250) and (0,0,0)
        self.line_thickness = 5

    def set_scale(self, new_scale):
        self.scale = new_scale
        self.coords = CoordConverter(self.scale, self.viewport)

    def add_scale(self, d_scale):
        new_scale = (self.scale[0] + d_scale[0], self.scale[1] + d_scale[1])
        self.scale = new_scale
        self.coords = CoordConverter(self.scale, self.viewport)

    def in_viewport(self, line):  # pos need to be in real coordinates(rc) and pygame has it automatically checked

        (pos1, pos2) = line
        (xp1, yp1) = self.coords.from_universe(pos1)
        (xp2, yp2) = self.coords.from_universe(pos2)

        ((xv1, yv1), (xv2, yv2)) = self.viewport
        xd = xv2 - xv1
        yd = yv2 - yv1

        if(((0 <= xp1 <= xd) and (0 <= yp1 <= yd)) or ((0 <= xp2 <= xd) and (0 <= yp2 <= yd))):
            return True
        return False

    def move_h(self, mult):
        ((x1, y1),(x2, y2)) = self.viewport
        displacement = self.speed * mult
        self.viewport = ((x1 + displacement, y1),(x2 + displacement, y2))
        self.coords = CoordConverter(self.scale, self.viewport)

    def move_v(self, mult):
        ((x1, y1),(x2, y2)) = self.viewport
        displacement = self.speed * mult
        self.viewport = ((x1, y1 + displacement),(x2, y2 + displacement))
        self.coords = CoordConverter(self.scale, self.viewport)

    def move_viewport(self, displacement_x: 0, displacement_y: 0):
        ((x1, y1), (x2, y2)) = self.viewport
        self.viewport = ((x1 + displacement_x, y1 + displacement_y), (x2 + displacement_x, y2 + displacement_y))
        self.coords = CoordConverter(self.scale, self.viewport)

    def draw(self, surface):
        for line in surface:
            # if(self.in_viewport(line)):  # pygame has it automatically checked so don't use it here
            pos1 = self.coords.from_universe(line[0])
            pos2 = self.coords.from_universe(line[1])
            pygame.draw.line(self.screen, self.color, pos1, pos2, self.line_thickness)

    def draw_player(self, player):
        pos1 = self.coords.from_universe(player.location)
        player_hit_box_x = player.hit_box[0] / self.scale[0]
        player_hit_box_y = player.hit_box[1] / self.scale[1]
        pygame.draw.rect(self.screen, self.color, (pos1[0], pos1[1], player_hit_box_x, player_hit_box_y), 0, 1)

    def adjust_viewport(self, camera):
        c_loc = camera.location
        ((x1, y1), (x2, y2)) = self.viewport
        scr_center = self.coords.to_universe(((x2 - x1)/2, (y2 - y1)/2))
        if c_loc != scr_center:
            displacement = (
                c_loc[0] - scr_center[0],
                c_loc[1] - scr_center[1]
            )
            self.move_viewport(displacement[0], displacement[1])

    def update_viewport(self, universe):
        self.camera.update(universe)
        self.adjust_viewport(self.camera)

    def update(self, universe):
        self.screen.fill((255,255,255))

        # adjust camera
        if universe.mode == "game":
            self.update_viewport(universe)

        # draw
        self.draw(universe.surface_altitudes)
        self.draw_player(universe.player)
