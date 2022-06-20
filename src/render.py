import pygame

from coords import CoordConverter


class Renderer:

    def __init__(self, screen, viewport, scale):
        self.coords = CoordConverter(scale, viewport)
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

    def update(self, universe):
        self.screen.fill((255,255,255))
        self.draw(universe.surface_altitudes)
        self.draw_player(universe.player)
