import pygame # Added import
from state import State
from settings import *

class Win(State):
    _font = None 
    def __init__(self):
        super().__init__()
        self.message = "You Win!"
        self.font    = None
        self._load_assets()
    def _load_assets(self):
        if Win._font is None:
            try:
                Win._font = pygame.font.Font("data/font/fsex2p00_public.ttf", 60)
                print("Win state font loaded.")
            except pygame.error as e:
                print(f"Error loading Win state font: {e}")
                Win._font = pygame.font.Font(None, 70) 
        self.font = Win._font
    def handle_enter(self, parameters):
        print("Entered Win State")
    def handle_keydown(self, key):
        if key in (K_RETURN, K_PAUSE_QUIT, K_BACKSPACE) and self.engine:
             self.engine.change_state('menu')
    def handle_erase(self, screen):
        screen.fill((0, 180, 0)) 
    def handle_draw(self, screen):
        if self.font:
            try:
                text_surf = self.font.render(self.message, True, WHITE)
                text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                screen.blit(text_surf, text_rect)
            except Exception as e:
                 print(f"Error drawing win message: {e}")