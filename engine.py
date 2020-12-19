import pygame
from settings import *

class Engine:
    states                = {}
    next_state            = None
    next_state_parameters = None
    state                 = None
    running               = False

    screen = pygame.display.set_mode(screen_size)

    def __init__(self,
            states,
            first_state,
            first_state_parameters,
            screen_size,
            window_title="Game Engine"
            ):
        pygame.display.set_caption(window_title)
        self.states = states
        self.state  = self.states[first_state]
        self.state.set_engine(self)
        self.state.handle_enter(first_state_parameters)

    def run(self,):
        self.running = True
        update_clock = pygame.time.Clock()

        while self.running:
            if self.next_state is not None:
                next_state = self.next_state
                self.state.handle_exit()
                self.state = self.states[self.next_state]
                self.state.set_engine(self)
                self.state.handle_enter(self.next_state_parameters)
                if self.next_state == next_state:
                    self.next_state            = None
                    self.next_state_parameters = None
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    self.state.handle_key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.state.handle_key_up(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.state.handle_mouse_button_down(event.button, event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.state.handle_mouse_button_up(event.button, event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.state.handle_mouse_motion(event.rel, event.pos, event.buttons)
                else:
                    pass
            self.state.handle_erase(self.screen)
            self.state.handle_update(update_clock.tick())
            self.state.handle_draw(self.screen)

            pygame.display.update()

    def change_state(self, new_state, parameters={}):
        self.next_state            = new_state
        self.next_state_parameters = parameters

    def exit(self):
        self.running = False






