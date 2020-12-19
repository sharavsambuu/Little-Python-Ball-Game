# coding: utf-8
from State import State
import pygame
from Settings import *
from random import randint

# Menu syntax
#
# menu: 
#  [ menuitem 1, menuitem 2, ..., menuitem n ]
# menuitems (titles must be strings):
#  link:                 (title, state name)
#  link with parameters: (title, state name, {key1:val1, key2:val2, ..., keyn:valn})
#  selection:            (title, (option1, option2, option3))
#  submenu:              (title, menu)

class Menu(State):
    
    MENU_QUIT = 'Menu item "quit"'
    
    menu = []
    choice = 0    
    path = []
    
    def __init__(self, menu, rememberPosition = False):
        State.__init__(self)
        self.menu = menu
        self.choice = 0
        self.rememberPosition = rememberPosition
        
        self.timer = 0.
        self.random_color = (randint(0,255), randint(0,255), randint(0,255))
        self.random_pos = (randint(0,screen_size[0]-1), randint(0,screen_size[1]-1))
        self.random_size = (screen_size[0]-1-randint(self.random_pos[0],screen_size[0]-1),
                            screen_size[1]-1-randint(self.random_pos[1],screen_size[1]-1))
        
    def handle_enter(self, parameters):        
        if not self.rememberPosition:
            self.path = []
            self.choice = 0             
        
    def handle_exit(self):
        pass
    
    def handle_key_down(self, key):
        currentMenu = self.currentMenu()
        selectedKey = currentMenu[self.choice][0]
        selectedItem = currentMenu[self.choice][1]
        
        if key == pygame.K_UP:
            if self.choice != 0:
                self.choice -= 1            

        elif key == pygame.K_DOWN:
            if self.choice < len(currentMenu) - 1:
                self.choice += 1

        elif key == pygame.K_ESCAPE or key == pygame.K_BACKSPACE:
            if len(self.path) > 0:
                self.path.pop()
            else:
                self.engine.exit()
            
        elif key == pygame.K_RETURN:
            if selectedItem is self.MENU_QUIT:
                self.engine.exit()
            elif type(selectedItem) is list:
                self.path.append(self.choice)
                self.choice = 0
            elif type(selectedItem) is str:
                options = {}
                if len(currentMenu[self.choice]) == 3:
                    options = currentMenu[self.choice][2]
                
                self.parse_options(self.menu, options)
                self.engine.change_state(selectedItem, options)
                    
        elif key == pygame.K_RIGHT:
            if type(selectedItem) is tuple:
                currentMenu[self.choice] = (selectedKey, selectedItem[1:] + selectedItem[:1])
        elif key == pygame.K_LEFT:
            if type(selectedItem) is tuple:
                currentMenu[self.choice] = (selectedKey, selectedItem[-1:] + selectedItem[:-1])
            
    def handle_update(self, timeDelta):
        self.timer += timeDelta/1000.
        if self.timer>2:
            self.random_color = (randint(0,255), randint(0,255), randint(0,255))
            self.random_pos = (randint(0,screen_size[0]-1), randint(0,screen_size[1]-1))
            self.random_size = (screen_size[0]-1-randint(self.random_pos[0],screen_size[0]-1),
                                screen_size[1]-1-randint(self.random_pos[1],screen_size[1]-1))
            self.timer = 0.
        pass
    
    def handle_draw(self, screen):
        screenFont = pygame.font.Font("data/font/fsex2p00_public.ttf", 35)
        screen.fill((0,0,0))
        pygame.draw.rect(screen, self.random_color, Rect(self.random_pos, self.random_size))        
        for i, text in enumerate([a[0] for a in self.currentMenu()]):
            item = self.currentMenu()[i][1]
            if type(item) is tuple:
                text = '%s: %s' % (text, str(item[0]))
            menuItem = None
            if i == self.choice:
                menuItem = screenFont.render(text, True, (255,0,0))
            else:
                menuItem = screenFont.render(text, True, (255,255,255))                
            screen.blit(menuItem, (20, 30 * i+35))       
        
        
    def currentMenu(self):
        current = self.menu
        for i in self.path:
            current = current[i][1]            
        return current
    
    def parse_options(self, menu, options):
        for menuItem in menu:
            key = menuItem[0]
            item = menuItem[1]
            if type(item) is list:
                self.parse_options(item, options)
            elif type(item) is tuple:
                options[key] = item[0]
                