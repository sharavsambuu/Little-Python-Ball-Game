from random import randint
import pygame
from state import State
from settings import *


class Menu(State):
    MENU_QUIT = 'Menu item "quit"'
    menu      = []
    choice    = 0
    path      = []

    def __init__(self, menu, remember_position = False):
        State.__init__(self)
        self.menu             = menu
        self.choice           = 0
        self.remember_position = remember_position

        self.timer        = 0.
        self.random_color = (randint(0,255), randint(0,255), randint(0,255))
        self.random_pos   = (randint(0,screen_size[0]-1), randint(0,screen_size[1]-1))
        self.random_size  = (screen_size[0]-1-randint(self.random_pos[0],screen_size[0]-1),
                             screen_size[1]-1-randint(self.random_pos[1],screen_size[1]-1))
        self.screen_font  = pygame.font.Font("data/font/fsex2p00_public.ttf", 35)

    def handle_enter(self, parameters):
        if not self.remember_position:
            self.path   = []
            self.choice = 0

    def handle_exit(self):
        pass

    def handle_key_down(self, key):
        current_menu  = self.current_menu()
        selected_key  = current_menu[self.choice][0]
        selected_item = current_menu[self.choice][1]

        if key == pygame.K_UP:
            if self.choice != 0:
                self.choice -= 1

        elif key == pygame.K_DOWN:
            if self.choice < len(current_menu) - 1:
                self.choice += 1

        elif key == pygame.K_ESCAPE or key == pygame.K_BACKSPACE:
            if len(self.path) > 0:
                self.path.pop()
            else:
                self.engine.exit()

        elif key == pygame.K_RETURN:
            if selected_item is self.MENU_QUIT:
                self.engine.exit()
            elif type(selected_item) is list:
                self.path.append(self.choice)
                self.choice = 0
            elif type(selected_item) is str:
                options = {}
                if len(current_menu[self.choice]) == 3:
                    options = current_menu[self.choice][2]

                self.parse_options(self.menu, options)
                self.engine.change_state(selected_item, options)

        elif key == pygame.K_RIGHT:
            if type(selected_item) is tuple:
                current_menu[self.choice] = (selected_key, selected_item[1:] + selected_item[:1])
        elif key == pygame.K_LEFT:
            if type(selected_item) is tuple:
                current_menu[self.choice] = (selected_key, selected_item[-1:] + selected_item[:-1])

    def handle_update(self, delta_time):
        self.timer += delta_time/1000.
        if self.timer>2:
            self.random_color = (randint(0,255), randint(0,255), randint(0,255))
            self.random_pos   = (randint(0, screen_size[0]-1), randint(0, screen_size[1]-1))
            self.random_size  = (screen_size[0]-1-randint(self.random_pos[0], screen_size[0]-1),
                                 screen_size[1]-1-randint(self.random_pos[1], screen_size[1]-1))
            self.timer        = 0.
        pass

    def handle_draw(self, screen):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, self.random_color, Rect(self.random_pos, self.random_size))
        for i, text in enumerate([a[0] for a in self.current_menu()]):
            item = self.current_menu()[i][1]
            if type(item) is tuple:
                text = '%s: %s' % (text, str(item[0]))
            menu_item = None
            if i == self.choice:
                menu_item = self.screen_font.render(text, True, (255,0,0))
            else:
                menu_item = self.screen_font.render(text, True, (255,255,255))
            screen.blit(menu_item, (20, 30 * i+35))

    def current_menu(self):
        current = self.menu
        for i in self.path:
            current = current[i][1]
        return current

    def parse_options(self, menu, options):
        for menu_item in menu:
            key  = menu_item[0]
            item = menu_item[1]
            if type(item) is list:
                self.parse_options(item, options)
            elif type(item) is tuple:
                options[key] = item[0]
