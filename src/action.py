from universe import Universe
from render import Renderer


class Action:
    # pylint: disable=no-self-use
    def is_done(self):
        return False

    def change_universe(self, universe: Universe, render: Renderer):  #
        pass

    # def change_renderer(self, render: Renderer):
    #     pass


class DoneAction(Action):
    def is_done(self):
        return True


class NopAction(Action):
    pass


class DebugAction(Action):
    def __init__(self, message):
        self.message = message

    def change_universe(self, universe, render):
        print(self.message)


class ChangeModeAction(Action):
    def __init__(self, mode):
        self.mode = mode

    def change_universe(self, universe, render):
        universe.mode = self.mode


class AddBlockAction(Action):
    def change_universe(self, universe, render):
        pass


class MoveActionNormalize(Action):  # normalized movement, can even work with joystick.
    def __init__(self, direction):
        self.direction = direction

    def change_universe(self, universe, render):
        universe.player.direction = \
            (universe.player.direction[0] + self.direction[0],
             universe.player.direction[1] + self.direction[1])


class MoveActionH(Action):  # can move only horizontally
    def __init__(self, direction_h):
        self.direction_h = direction_h

    def wall(self, universe):
        pass

    def change_universe(self, universe, render):
        universe.player.direction_h = self.direction_h
        universe.player.move_h()


class MoveActionV(Action):  # can move only vertically
    def __init__(self, direction_y):
        self.direction_y = direction_y

    def wall(self, universe):
        pass

    def change_universe(self, universe, render):
        universe.player.direction_y = self.direction_y
        universe.player.move_v()


class RunAction(Action):
    def change_universe(self, universe, render):
        print("run")
        universe.player.state = "running"
        universe.player.run = universe.player.run_on


class StopRunAction(Action):
    def change_universe(self, universe, render):
        print("stop running")
        universe.player.state = "standing"
        universe.player.run = universe.player.run_off


class StandAction(Action):
    def change_universe(self, universe, render):
        universe.player.state = "standing"
        print("standing")


class PressedArrowH(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_universe(self, universe, render):
        # print("moving viewport")
        render.move_h(self.direction)


class PressedArrowV(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_universe(self, universe, render):
        # print("moving viewport")
        render.move_v(self.direction)


class ZoomIn(Action):  # TODO fix: a fraction to whole number conversion so position is a whole number
    def change_universe(self, universe, render):
        render.add_scale((0.01,0.01))


class ZoomOut(Action):  # TODO fix: a fraction to whole number conversion so position is a whole number
    def change_universe(self, universe, render):
        if render.scale != (1,1):
            render.add_scale((-0.01,-0.01))


class OnOffGrid(Action):  # turns on/off grid for building maps
    def change_universe(self, universe, render):
        universe.edit.set_grid()
        print("Grid: ", universe.edit.grid)


class ChangeBodie(Action):
    def change_universe(self, universe, render):
        universe.edit.set_bodie()
        print("Edit set to Bodie")


class ChangeGroup(Action):
    def change_universe(self, universe, render):
        universe.edit.set_group()
        print("Edit set to Group")


class ChangeSelectGroup(Action):
    def change_universe(self, universe, render):
        universe.edit.set_select_group()
        print("Edit set to select Group")


class ChangeRemoveGroup(Action):
    def change_universe(self, universe, render):
        universe.edit.set_remove_group()
        print("Edit set to remove Group")


class ChangeRemoveBodie(Action):
    def change_universe(self, universe, render):
        universe.edit.set_remove_bodie()
        print("Edit set to remove Bodie")


class Click(Action):
    def change_universe(self, universe, render):
        map_list = {
            "group":StartGroup().change_universe, 
            "bodie":StartBodie().change_universe, 
            "select_group":SelectGroup().change_universe,
            "remove_group":RemoveGroup().change_universe,
            "remove_bodie":RemoveBodie().change_universe,
        }

        if map_list.get(universe.edit.bodie_type):
            map_list[universe.edit.bodie_type](universe, render)


class Unclick(Action):
    def change_universe(self, universe, render):
        map_list = {
            "group":FinishGroup().change_universe, 
            "bodie":FinishBodie().change_universe
        }

        if map_list.get(universe.edit.bodie_type):
            map_list[universe.edit.bodie_type](universe, render)


class SelectGroup(Action):
    def change_universe(self, universe, render):
        print("finding group")
        group = universe.find_selected_group()
        universe.set_edit_main_group(group)
        print(id(universe.edit.main_group), type(universe.edit.main_group))


class StartGroup(Action):
    def change_universe(self, universe, render):
        universe.edit.start = universe.edit.get_mouse_pos(universe.mouse.location)
        print("Group start is at pos: ", universe.edit.start)


class FinishGroup(Action):
    def change_universe(self, universe, render):
        universe.add_group()


class StartBodie(Action):
    def change_universe(self, universe, render):
        print(id(universe.edit.main_group), type(universe.edit.main_group))
        if universe.edit.main_group:
            universe.edit.start = universe.edit.get_mouse_pos(universe.mouse.location)
            print("Bodie start is at pos: ", universe.edit.start)
        else:
            print("ERROR: empty group. Choose group first")

class FinishBodie(Action):
    def change_universe(self, universe, render):
        if universe.edit.main_group:
            universe.add_bodie_to_group()
        else:
            print("ERROR: empty group. Choose group first")


class RemoveGroup(Action):
    def change_universe(self, universe, render):
        universe.remove_group()


class RemoveBodie(Action):
    def change_universe(self, universe, render):
        if universe.edit.main_group:
            universe.remove_body()
        else:
            print("Please select group first")

