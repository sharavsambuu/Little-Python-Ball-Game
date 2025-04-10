import pygame 

class State:
    def __init__(self):
        self.engine = None
    def set_engine(self, engine):
        self.engine = engine
    def handle_enter(self, parameters):
        pass
    def handle_exit(self):
        pass
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
        elif event.type == pygame.KEYUP:
            self.handle_keyup(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down(event.button, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up(event.button, event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event.rel, event.pos, event.buttons)
    def handle_keydown(self, key):
        pass
    def handle_keyup(self, key):
        pass
    def handle_mouse_button_down(self, button, position):
        pass
    def handle_mouse_button_up(self, button, position):
        pass
    def handle_mouse_motion(self, relative, position, buttons):
        pass
    def handle_update(self, delta_time):
        pass
    def handle_erase(self, screen):
        pass
    def handle_draw(self, screen):
        pass