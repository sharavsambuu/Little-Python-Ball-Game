import pygame
from random import randint
from state import State
from settings import *

class Menu(State):
    MENU_QUIT = 'MENU_ITEM_QUIT'
    MENU_BACK = 'MENU_ITEM_BACK' 
    _font     = None
    def __init__(self, menu_structure, remember_position=False):
        super().__init__()
        self.menu_structure    = [list(item) if isinstance(item[1], (list, tuple)) else list(item) for item in menu_structure]
        self.choice            = 0 
        self.path              = [] 
        self.remember_position = remember_position 
        self.timer             = 0.0
        self.random_color      = self._get_random_color()
        self.random_rect       = self._get_random_rect()
        self.font              = None
        self._load_assets()
    def _load_assets(self):
         if Menu._font is None:
             try:
                 Menu._font = pygame.font.Font("data/font/fsex2p00_public.ttf", 35)
                 print("Menu font loaded.")
             except pygame.error as e:
                 print(f"Error loading font for Menu state: {e}")
                 Menu._font = pygame.font.Font(None, 40) 
         self.font = Menu._font 
    def _get_random_color(self):
        return (randint(50, 200), randint(50, 200), randint(50, 200))
    def _get_random_rect(self):
        max_w = max(100, SCREEN_WIDTH // 2)
        max_h = max(100, SCREEN_HEIGHT // 2)
        w     = randint(max_w // 2, max_w)
        h     = randint(max_h // 2, max_h)
        x     = randint(0, SCREEN_WIDTH - w)
        y     = randint(0, SCREEN_HEIGHT - h)
        return pygame.Rect(x, y, w, h)
    def _current_menu_level(self):
        level = self.menu_structure
        try:
            for index in self.path:
                 item_data = level[index]
                 if len(item_data) > 1 and isinstance(item_data[1], list):
                     level = item_data[1] 
                 else:
                     print(f"Warning: Invalid menu path at index {index}. Item: {item_data}")
                     self.path = self.path[:self.path.index(index)] 
                     level = self.menu_structure
                     for valid_index in self.path:
                          level = level[valid_index][1]
                     break 
        except IndexError:
             print(f"Warning: Menu path index out of range. Path: {self.path}")
             self.path = [] 
             level = self.menu_structure 
        except Exception as e:
             print(f"Error navigating menu structure: {e}")
             self.path = []
             level = self.menu_structure
        return level
    def _parse_options(self, current_structure, options_dict):
        for item_data in current_structure:
             # Item Data Format: [Title, Action/Submenu/Options, [Params]]
             if not isinstance(item_data, list) or len(item_data) < 2: continue
             title      = item_data[0]
             item_value = item_data[1]
             if isinstance(item_value, list):
                 self._parse_options(item_value, options_dict)
             elif isinstance(item_value, tuple):
                 if item_value: 
                      options_dict[title] = item_value[0]

    def handle_enter(self, parameters):
        print("Entering Menu State")
        self.remember_position = parameters.get('remember_position', False)
        if not self.remember_position:
            self.path = []
            self.choice = 0
        self.remember_position = False
    def handle_exit(self):
        print("Exiting Menu State")
        pass 
    def handle_keydown(self, key):
        current_level = self._current_menu_level()
        if not current_level:
             print("Menu Error: No items at current level.")
             return 
        num_items = len(current_level)
        if num_items == 0: return 
        if key == pygame.K_UP:
            self.choice = (self.choice - 1 + num_items) % num_items 
        elif key == pygame.K_DOWN:
            self.choice = (self.choice + 1) % num_items
        elif key == K_BACKSPACE or key == K_PAUSE_QUIT: 
            if self.path: 
                self.path.pop() 
                self.choice = 0 
            else: 
                 print("At top level, Esc/Backspace does nothing (or could exit).")
                 pass
        elif key == K_RETURN: 
            if 0 <= self.choice < num_items:
                selected_item_data = current_level[self.choice]
                title  = selected_item_data[0]
                action = selected_item_data[1]
                params = selected_item_data[2] if len(selected_item_data) > 2 else {}
                if action == self.MENU_QUIT:
                    if self.engine: self.engine.exit()
                elif action == self.MENU_BACK: 
                     if self.path:
                         self.path.pop()
                         self.choice = 0
                elif isinstance(action, list): 
                    self.path.append(self.choice) 
                    self.choice = 0 
                elif isinstance(action, str): 
                    if self.engine:
                        all_options = {}
                        self._parse_options(self.menu_structure, all_options)
                        final_params = {**all_options, **params}
                        self.engine.change_state(action, final_params)
                elif isinstance(action, tuple): 
                     print(f"Selected option '{title}', no action on Enter.")
                     pass
            else:
                 print(f"Error: Invalid menu choice index {self.choice}")
        elif key == pygame.K_RIGHT or key == pygame.K_LEFT:
             if 0 <= self.choice < num_items:
                selected_item_data = current_level[self.choice]
                action = selected_item_data[1]
                if isinstance(action, tuple) and len(action) > 1: 
                     current_options = list(action) 
                     if key == pygame.K_RIGHT:
                         new_options_list = current_options[1:] + current_options[:1]
                     else: 
                         new_options_list = current_options[-1:] + current_options[:-1]
                     current_level[self.choice][1] = tuple(new_options_list)
                     print(f"Option '{selected_item_data[0]}' changed to: {new_options_list[0]}")
    def handle_update(self, delta_time):
        self.timer += delta_time
        if self.timer > 1.5: 
            self.random_color = self._get_random_color()
            self.random_rect  = self._get_random_rect()
            self.timer        = 0.0 
    def handle_erase(self, screen):
        screen.fill(BLACK)
    def handle_draw(self, screen):
        try:
            pygame.draw.rect(screen, self.random_color, self.random_rect)
        except Exception as e: 
             print(f"Error drawing random rect: {e}")
             self.random_rect = self._get_random_rect() 
        current_level = self._current_menu_level()
        start_y       = 80 
        line_spacing  = 50 
        if not self.font: 
            print("Error: Menu font not available for drawing.")
            return
        for i, item_data in enumerate(current_level):
            if not isinstance(item_data, list) or len(item_data) < 1: continue 
            title  = item_data[0]
            action = item_data[1] if len(item_data) > 1 else None
            display_text = str(title) 
            if isinstance(action, tuple):
                 if action: 
                    display_text = f"{title}: < {action[0]} >" 
                 else:
                    display_text = f"{title}: (No Options)"
            text_color = YELLOW if i == self.choice else WHITE 
            try:
                text_surface = self.font.render(display_text, True, text_color)
                text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH / 2,
                                                  top=start_y + i * line_spacing)
                screen.blit(text_surface, text_rect)
            except pygame.error as e:
                print(f"Error rendering menu item '{display_text}': {e}")
            except Exception as e: 
                 print(f"Unexpected error rendering menu item: {e}")