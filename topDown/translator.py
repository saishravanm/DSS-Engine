import pygame


class Translator:

    def __init__(self, translation_map, done_action):
        self.translation_map = translation_map
        self.done_action = done_action

    def _get_map(self, mode, key):
        return self.translation_map.get(mode, {}).get(key, {})

    def translate_event(self, mode, event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return [self.done_action]

        if event.type == pygame.KEYDOWN:
            action = self._get_map(mode, 'key_down').get(event.key)
            if action:
                return [action]

        if event.type == pygame.KEYUP:
            action = self._get_map(mode, 'key_up').get(event.key)
            if action:
                return [action]

        return []

    def translate_pressed(self, mode):
        key_pressed = self._get_map(mode, 'key_pressed')
        key_not_pressed = self._get_map(mode, 'key_not_pressed')
        mouse_pressed = self._get_map(mode, 'mouse_pressed')
        mouse_not_pressed = self._get_map(mode, 'mouse_not_pressed')

        pressed = pygame.key.get_pressed()
        pressedM = pygame.mouse.get_pressed()

        return (
                [action for key, action in key_pressed.items() if pressed[key]] +
                [action for key, action in key_not_pressed.items() if not pressed[key]] +
                [action for button, action in mouse_pressed.items() if pressedM[button]] +
                [action for button, action in mouse_not_pressed.items() if not pressedM[button]]
        )
