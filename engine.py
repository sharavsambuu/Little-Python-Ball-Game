import pygame
from settings import SCREEN_SIZE

class Engine:
    def __init__(self,
                 states,
                 first_state_key,
                 first_state_params,
                 window_title="Game Engine"):

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(window_title)

        self.states        = states
        self.current_state = self.states[first_state_key]
        self.current_state.set_engine(self)
        self.current_state.handle_enter(first_state_params if first_state_params else {})

        self.next_state_key    = None
        self.next_state_params = None
        self.running           = False
        self.clock             = pygame.time.Clock()

    def run(self):
        self.running = True

        while self.running:
            if self.next_state_key is not None:
                target_state_key = self.next_state_key
                target_params    = self.next_state_params if self.next_state_params else {}

                self.current_state.handle_exit()
                print(f"Transitioning from {type(self.current_state).__name__} to {target_state_key}") 
                self.current_state = self.states[target_state_key]
                self.current_state.set_engine(self)
                self.current_state.handle_enter(target_params)

                self.next_state_key    = None
                self.next_state_params = None

            events = pygame.event.get() 
            for event in events:
                if event.type == pygame.QUIT:
                    self.exit()
                self.current_state.handle_event(event)

            delta_time_ms = self.clock.tick(60) 
            delta_time_s  = delta_time_ms / 1000.0 

            self.current_state.handle_erase(self.screen)

            self.current_state.handle_update(delta_time_s) 

            self.current_state.handle_draw(self.screen)

            pygame.display.flip() 

    def change_state(self, new_state_key, parameters=None):
        print(f"Change state requested: {new_state_key} with params {parameters}") 
        if new_state_key not in self.states:
            print(f"Warning: Attempted to change to unknown state '{new_state_key}'")
            return
        if parameters is None:
            parameters = {}
        self.next_state_key    = new_state_key
        self.next_state_params = parameters

    def exit(self):
        print("Exit requested.")
        self.running = False