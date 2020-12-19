# coding: utf-8
import pygame, time, pygame.key, sys, os
from pygame.locals import *
from Settings import *


#дэлгэцийн төвд нь тоглоомын цонхыг аваачих
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

import pygame

class Engine:
    states = {}
    nextState = None
    nextStateParameters = None
    state = None
    running = False    
    screen = pygame.display.set_mode(screen_size)
    
    # Байгуулагч
    def __init__(self, states, firstState, firstStateParameters, screenSize, window_title='GameEngine'):
        #self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption(window_title)
        self.states = states
        self.state = self.states[firstState]
        self.state.set_engine(self)
        self.state.handle_enter(firstStateParameters)        
        
    def run(self):
        self.running = True
        updateClock = pygame.time.Clock()
        
        while self.running:
            # state шилжилт
            if self.nextState is not None:
                next = self.nextState
                self.state.handle_exit()
                self.state = self.states[self.nextState]
                self.state.set_engine(self)
                self.state.handle_enter(self.nextStateParameters)
                if self.nextState is next:
                    self.nextState = None
                    self.nextStateParameters = None
            # Оролт боловсруулах
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.exit()
                elif event.type is pygame.KEYDOWN:
                    self.state.handle_key_down(event.key)
                elif event.type is pygame.KEYUP:
                    self.state.handle_key_up(event.key)
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    self.state.handle_mouse_button_down(event.button, event.pos)
                elif event.type is pygame.MOUSEBUTTONUP:
                    self.state.handle_mouse_button_up(event.button, event.pos)
                elif event.type is pygame.MOUSEMOTION:
                    self.state.handle_mouse_motion(event.rel, event.pos, event.buttons)
                else:
                    pass
            # өгөгдүүлээ шинэчлээд тэднийгээ зурах
            self.state.handle_erase(self.screen)
            self.state.handle_update(updateClock.tick())
            self.state.handle_draw(self.screen)
            
            # pygame-ийн арын буффер дээр зурсан өгөгдлүүдийг дэлгэцийн буферлүү хийнэ
            pygame.display.update()
                
    def change_state(self, newState, parameters = {}):
        self.nextState = newState
        self.nextStateParameters = parameters
        
    def exit(self):
        self.running = False
        
