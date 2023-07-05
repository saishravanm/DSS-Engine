import pygame

from action import *


FPS = 60
HOR_SPEED = 12

TRANSLATION_MAP = {
    'game': {
        'key_pressed': {
            # add some methods that are executed when key is pressed
            pygame.K_LEFT: MoveActionNormalize((0, -1)),
            pygame.K_RIGHT: MoveActionNormalize((0, 1)),
            pygame.K_UP: MoveActionNormalize((1, 0)),
            pygame.K_DOWN: MoveActionNormalize((-1, 0)),
            # pygame.K_LEFT: MoveActionH(-1),
            # pygame.K_RIGHT: MoveActionH(1),
            # pygame.K_UP: MoveActionV(-1),
            # pygame.K_DOWN: MoveActionV(1),
            pygame.K_LSHIFT: RunAction(),
            # pygame.KMOD_NONE: StandAction()  # don't use it
            pygame.K_1: ZoomIn(),
            pygame.K_2: ZoomOut(),
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
            pygame.K_LSHIFT: StopRunAction()
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
            pygame.K_g: OnOffGrid(),
            pygame.K_1: ChangeGroup(),
            pygame.K_2: ChangeBodie(),
        },
        'key_not_pressed': {
            # add some methods that are executed when key is not pressed
        },
        'key_down': {
            # add some methods that are executed when key is down pressed
            pygame.K_e: ChangeModeAction("game"),
            pygame.K_q: Click(),
        },
        'key_up': {
            # add some methods that are executed when key is up pressed
            pygame.K_q: Unclick(),
        },
        'mouse_pressed': {
            # add some methods that are executed when mouse key is pressed
        },
        'mouse_not_pressed': {
            # add some methods that are executed when mouse key is not pressed
        }
    }
}
