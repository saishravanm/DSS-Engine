import pygame

from action import *


FPS = 600
HOR_SPEED = 12

TRANSLATION_MAP = {
    'game': {
        'key_pressed': {
            # add some methods that are executed when key is pressed
            pygame.K_LEFT: MoveAction(-1),
            pygame.K_RIGHT: MoveAction(1),
            pygame.K_LSHIFT: RunAction(),
            # pygame.KMOD_NONE: StandAction()
        },
        'key_not_pressed': {
            # add some methods that are executed when key is not pressed
        },
        'key_down': {
            # add some methods that are executed when key is down pressed
            pygame.K_e: ChangeModeAction("map"),
            # pygame.K_LSHIFT: RunAction(),
        },
        'key_up': {
            # add some methods that are executed when key is up pressed
            # pygame.K_LSHIFT: StopRunAction()
        },
        'mouse_pressed': {
            # add some methods that are executed when mouse key is pressed
        },
        'mouse_not_pressed': {
            # add some methods that are executed when mouse key is not pressed
        }
    },
    'map': {
        'key_pressed': {
            # add some methods that are executed when key is pressed
            # pygame.K_UP: DebugAction("Pressed UP"),
            pygame.K_UP: PressedArrowV(-1),
            # pygame.K_DOWN: DebugAction("Pressed DOWN"),
            pygame.K_DOWN: PressedArrowV(1),
            # pygame.K_LEFT: DebugAction("Pressed LEFT"),
            pygame.K_LEFT: PressedArrowH(-1),
            # pygame.K_RIGHT: DebugAction("Pressed Right"),
            pygame.K_RIGHT: PressedArrowH(1),

        },
        'key_not_pressed': {
            # add some methods that are executed when key is not pressed
        },
        'key_down': {
            # add some methods that are executed when key is down pressed
            pygame.K_e: ChangeModeAction("game"),
        },
        'key_up': {
            # add some methods that are executed when key is up pressed
        },
        'mouse_pressed': {
            # add some methods that are executed when mouse key is pressed
        },
        'mouse_not_pressed': {
            # add some methods that are executed when mouse key is not pressed
        }
    }
}
