from universe import Universe
from render import Renderer


class Action:
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


class MoveAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def wall(self, universe):
        pass

    def change_universe(self, universe, render):
        universe.player.direction = self.direction
        universe.player.move()


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
        render.move_H(self.direction)


class PressedArrowV(Action):
    def __init__(self, direction):
        self.direction = direction

    def change_universe(self, universe, render):
        # print("moving viewport")
        render.move_V(self.direction)
