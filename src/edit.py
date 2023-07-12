

class Edit:
    def __init__(self):
        self.bodie_type = "group"
        self.main_group = None
        self.start = (0,0)
        self.grid = False
        self.grid_size = 20

    def set_group(self):
        self.bodie_type = "group"
        self.start = (0,0)

    def set_bodie(self):
        self.bodie_type = "bodie"

    def set_select_group(self):
        self.bodie_type = "select_group"
        self.main_group = None

    def set_grid(self):
        self.grid = not self.grid

    def get_mouse_pos(self, mouse_pos):
        if self.grid:
            x = round(mouse_pos[0] / self.grid_size) * self.grid_size
            y = round(mouse_pos[1] / self.grid_size) * self.grid_size
            print(x, y)
            return (x, y)
        else:
            return mouse_pos

    def add_group(self, group, group_list):
        pass

    def add_bodi_to_group(self):
        pass

