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


class MoveActionNormalize(Action):  # normalized movement, can even work with joystick. TODO finish function so it can work with V and H ath the same time
    def __init__(self, direction_h, direction_y):
        self.direction_h = direction_h
        self.direction_y = direction_y

    def wall(self, universe):
        pass

    def change_universe(self, universe, render):
        universe.player.direction_h += self.direction_h
        universe.player.direction_y += self.direction_y
        universe.player.move_normalize()


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
