

class Edit:
    def __init__(self):
        self.bodie_type = "group"
        self.main_group = None
        self.start = (0,0)

    def set_group(self):
        self.bodie_type = "group"
        self.start = (0,0)

    def set_bodie(self):
        self.bodie_type = "bodie"

    def set_select_group(self):
        self.bodie_type = "select_group"
        self.main_group = None

    def add_group(self, group, group_list):
        pass

    def add_bodi_to_group(self):
        pass

