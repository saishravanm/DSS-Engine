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
        self.viewport = ((x1 + self.speed * mult, y1),(x2 + self.speed * mult, y2))
        self.coords = CoordConverter(self.scale, self.viewport)

    def move_v(self, mult):
        ((x1, y1),(x2, y2)) = self.viewport
        self.viewport = ((x1, y1 + self.speed * mult),(x2, y2 + self.speed * mult))
        self.coords = CoordConverter(self.scale, self.viewport)

    def draw(self, surface):
        for line in surface:
            # if(self.in_viewport(line)):  # pygame has it automatically checked so don't use it here
            pos1 = self.coords.from_universe(line[0])
            pos2 = self.coords.from_universe(line[1])
            pygame.draw.line(self.screen, self.color, pos1, pos2, self.line_thickness)

    def draw_player(self, player):
        pos1 = self.coords.from_universe(player.location)
        pygame.draw.rect(self.screen, self.color, (pos1[0], pos1[1], player.hit_box[0], player.hit_box[1]), 0,1)
    def draw_wall(self, wall):  
        pygame.draw.line(self.screen,self.color,wall.starting_point,wall.ending_point,wall.thickness)