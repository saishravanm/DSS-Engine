import pygame
import math
from coords import CoordConverter
from camera import Camera


class Renderer:

    def __init__(self, screen, viewport, scale):
        self.coords = CoordConverter(scale, viewport)
        self.camera = Camera(self.coords.to_universe((viewport[1][0]/2, viewport[1][1]/2)), (0, 0), "follow_in_circle")
        self.screen = screen
        self.viewport = viewport
        self.scale = scale
        self.speed = 5
        self.color = (250,0,0)  # (250,250,250) and (0,0,0)
        self.line_thickness = 5
        self.MAX_DEPTH = 1000

        # EXPERIMENTAL
        self.draw_gen_obj_map = {"rect":self.draw_gen_obj_rect_2, "circle":self.draw_gen_obj_circle}

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

    def move_viewport(self, displacement_x=0, displacement_y=0):
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

    def draw_fov(self, player):
        # direction
        start_angle = -player.angle
        player_loc = (self.coords.from_universe(player.location))  # convert player universe location to screen location
        pygame.draw.line(self.screen, (49, 20, 179), (player_loc[0], player_loc[1]),
                         (player_loc[0] + math.cos(start_angle) * 50,
                          player_loc[1] - math.sin(start_angle) * 50), 3)

        pygame.draw.line(self.screen, (49, 20, 179), (player_loc[0], player_loc[1]),
                         (player_loc[0] + math.cos(start_angle - player.HALF_FOV) * 50,
                          player_loc[1] - math.sin(start_angle - player.HALF_FOV) * 50), 3)

        pygame.draw.line(self.screen, (49, 20, 179), (player_loc[0], player_loc[1]),
                         (player_loc[0] + math.cos(start_angle + player.HALF_FOV) * 50,
                          player_loc[1] - math.sin(start_angle + player.HALF_FOV) * 50), 3)

    def cast_rays(self,player):
        start_angle = (-player.angle) - player.HALF_FOV
        player_loc = (self.coords.from_universe(player.location))  # convert player universe location to screen location
        for ray in range(player.CASTED_RAYS):
            for depth in range(self.MAX_DEPTH):
                target_x = player_loc[0] + math.cos(start_angle) * depth
                target_y = player_loc[1] - math.sin(start_angle) * depth

                # draw casted ray
                pygame.draw.line(self.screen, (0, 255, 0), (player_loc[0],player_loc[1]), (target_x,target_y))

            start_angle += player.STEP_ANGLE

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
        # self.screen.fill((255,255,255))
        self.screen.fill((40, 40, 40))

        # adjust camera
        if universe.mode == "game":
            self.update_viewport(universe)

        # draw
        self.draw(universe.surface_altitudes)
        #if universe.mode == "game":
        #    self.cast_rays(universe.player)
        #    self.draw_fov(universe.player)
        self.draw_player(universe.player)
        self.draw_gen_obj_rect_2(universe.player.rigid_body)  # this is stupid, I will fix it latter

        # EXPERIMENTAL
        #self.draw_gen_obj(universe.physics.bodies)
        self.draw_groups(universe.physics.groups)

        if universe.mode == "map":
            self.draw_mouse_preview_in_editor(universe.edit, universe.mouse)

# ===================EXPERIMENTAL===================
    def draw_groups(self, groups_list):
        for group in groups_list:
            self.draw_gen_obj_map[group.shape.shape_type](group)
            self.draw_gen_obj(group.bodies) 

    def draw_gen_obj(self, gen_obj_list):
        for gen_obj in gen_obj_list:
            self.draw_gen_obj_map[gen_obj.shape.shape_type](gen_obj)

    def draw_gen_obj_rect(self, gen_obj):
        screen_pos = self.coords.from_universe(gen_obj.pos)
        pygame.draw.rect(self.screen, gen_obj.render_params.color, (screen_pos[0], screen_pos[1], gen_obj.shape.width, gen_obj.shape.height), gen_obj.render_params.thickness, gen_obj.render_params.curve)

    def draw_gen_obj_circle(self, gen_obj):
        screen_pos = self.coords.from_universe(gen_obj.pos)
        pygame.draw.circle(self.screen, gen_obj.render_params.color, screen_pos, gen_obj.shape.radius, gen_obj.render_params.thickness)

    def draw_gen_obj_rect_2(self, gen_obj):
        screen_pos = self.coords.from_universe(gen_obj.pos)

        sprite = pygame.Surface((gen_obj.shape.width, gen_obj.shape.height))
        sprite.set_colorkey(gen_obj.render_params.colorkey)
        sprite.fill(gen_obj.render_params.fill)

        pygame.draw.rect(sprite, gen_obj.render_params.color, (0, 0, gen_obj.shape.width - 2, gen_obj.shape.height - 2), 2)

        rotated = pygame.transform.rotate(sprite, gen_obj.angle)
        rect = rotated.get_rect()

        # self.screen.blit(rotated, (screen_pos[0] - rect.width / 2, screen_pos[1] - rect.height / 2))  # useful to draw slides or frames

        # pygame.draw.line(self.screen, (255, 0, 255), self.coords.from_universe(gen_obj.vertices[0]), self.coords.from_universe(gen_obj.vertices[1]))
        # pygame.draw.line(self.screen, (255, 0, 255), self.coords.from_universe(gen_obj.vertices[1]), self.coords.from_universe(gen_obj.vertices[2]))
        # pygame.draw.line(self.screen, (255, 0, 255), self.coords.from_universe(gen_obj.vertices[2]), self.coords.from_universe(gen_obj.vertices[3]))
        # pygame.draw.line(self.screen, (255, 0, 255), self.coords.from_universe(gen_obj.vertices[3]), self.coords.from_universe(gen_obj.vertices[0]))
        pygame.draw.line(self.screen, gen_obj.render_params.color, self.coords.from_universe(gen_obj.vertices[0]),
                         self.coords.from_universe(gen_obj.vertices[1]))
        pygame.draw.line(self.screen, gen_obj.render_params.color, self.coords.from_universe(gen_obj.vertices[1]),
                         self.coords.from_universe(gen_obj.vertices[2]))
        pygame.draw.line(self.screen, gen_obj.render_params.color, self.coords.from_universe(gen_obj.vertices[2]),
                         self.coords.from_universe(gen_obj.vertices[3]))
        pygame.draw.line(self.screen, gen_obj.render_params.color, self.coords.from_universe(gen_obj.vertices[3]),
                         self.coords.from_universe(gen_obj.vertices[0]))

    def draw_mouse_preview_in_editor(self, edit, mouse):
        screen_pos = self.coords.from_universe(edit.get_mouse_pos(mouse.location))
        pygame.draw.circle(self.screen, mouse.preview_color, screen_pos, mouse.preview_radius, mouse.preview_thikness)

# ==================================================
