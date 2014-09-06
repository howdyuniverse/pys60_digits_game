"""
    http://www.mobilenin.com/pys60/resources/ex_use_of_keys_descr.py
"""
import appuifw

class Keyboard(object):

    def __init__(self, onevent=lambda:None):
        self._keyboard_state = {}
        self._downs = {}
        self._onevent = onevent

    def handle_event(self, event):
        if event['type'] == appuifw.EEventKeyDown:
            code = event['scancode']
            if not self.is_down(code):
                self._downs[code]=self._downs.get(code, 0) + 1
            self._keyboard_state[code] = 1

        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']] = 0

        self._onevent()

    def is_down(self, scancode):
        return self._keyboard_state.get(scancode, 0)

    def pressed(self, scancode):
        if self._downs.get(scancode, 0):
            self._downs[scancode] -= 1
            return True
        return False

    def flush(self):
        for key in self._downs:
            self._downs[key] = 0
