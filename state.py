class State(object):
    engine = None
    def __init__(self):
        pass
    def set_engine(self, engine):
        self.engine = engine
    def handle_enter(self, parameters):
        pass
    def handle_exit(self):
        pass
    def handle_key_down(self, key):
        pass
    def handle_key_up(self, key):
        pass
    def handle_mouse_button_down(self, button, position):
        pass
    def handle_mouse_button_up(self, button, position):
        pass
    def handle_mouse_motion(self, relative, position, buttons):
        pass
    def handle_update(self, delta_time):
        pass
    def handle_eras(self, screen):
        pass
    def handle_draw(self, screen):
        pass
