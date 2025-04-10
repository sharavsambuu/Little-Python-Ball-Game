import pygame
from random import randint, uniform
from state import State
from settings import *
# Import the helper function correctly now
from game_object.game_object import load_image_asset


class Star:
    def __init__(self, x, y, speed):
        self.x     = x
        self.y     = y
        self.speed = speed

class About(State):
    def __init__(self):
        super().__init__()
        self.scroll_pos   = [SCREEN_WIDTH / 4, SCREEN_HEIGHT]
        self.scroll_speed = 20 
        self.text_color   = WHITE
        self.line_height  = 20
        self.images       = {}
        self.stars        = []
        self.delta_time   = 0.0 
        self.font         = None      
        self.music_path   = "data/sound/music/song12.ogg"
        self._load_assets()
        self.info_text = (
            "                    Тоглоомын тухай",
            "",
            "     Ашигласан хэл : Python - http://www.python.org",
            "     Ашигласан сан : PyGame - http://www.pygame.org",
            "                     Box2D  - http://www.box2d.org",
            "",
            "     Ашигласан IDE : VSCode",
            "     Ашигласан хөгжим : CrayonBall -ий авиа,",
            "                        http://www.8bc.org -ий хөгжим",
            "",
            "     Хөгжүүлэгч :",
            "           Г.Шаравсамбуу - sharavsambuu@gmail.com",
            "                          http://sharavaa.blogspot.com"
            "",
            "",
            "     2010 он",
            "",
            "",
            "",
            "",
        )
        for _ in range(200):
            self._add_star(x=uniform(0, SCREEN_WIDTH), y=uniform(0, SCREEN_HEIGHT))

    def _load_assets(self):
        try:
            self.font = pygame.font.Font("data/font/fsex2p00_public.ttf", 16)
        except pygame.error as e:
            print(f"Error loading font for About state: {e}")
            self.font = pygame.font.Font(None, 20) 
        self.images['box2d' ] = load_image_asset('data/image/logo/box2d.png')
        self.images['pygame'] = load_image_asset('data/image/logo/pygame.gif')
        self.images['python'] = load_image_asset('data/image/logo/python.png')

    def _add_star(self, x=None, y=None):
        if x is None: x = SCREEN_WIDTH
        if y is None: y = uniform(0, SCREEN_HEIGHT - 1)
        speed = uniform(10, 300)
        self.stars.append(Star(x, y, speed))

    def handle_enter(self, parameters):
        self.scroll_pos = [SCREEN_WIDTH / 4, SCREEN_HEIGHT]
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.7) 
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error loading/playing music '{self.music_path}' in About state: {e}")

    def handle_exit(self):
        pygame.mixer.music.stop()

    def handle_keydown(self, key):
        if key in (K_PAUSE_QUIT, K_RETURN, K_MOVE_LEFT, K_BACKSPACE) and self.engine:
            self.engine.change_state('menu')

    def handle_update(self, delta_time):
        self.delta_time     = delta_time 
        self.scroll_pos[1] -= self.scroll_speed * delta_time
        total_text_height   = len(self.info_text) * self.line_height
        logo_height = max(img.get_height() for img in self.images.values()) if self.images else 0
        if self.scroll_pos[1] + total_text_height + logo_height + 50 < 0:
            self.scroll_pos[1] = SCREEN_HEIGHT

        for star in self.stars:
            star.x -= star.speed * delta_time

        self.stars = [star for star in self.stars if star.x > -10] 

        if uniform(0, 1) < 0.5 * delta_time: 
             self._add_star()

    def handle_erase(self, screen):
        screen.fill(BLACK)

    def handle_draw(self, screen):
        # Draw stars
        star_blur_length = 0.05 
        for star in self.stars:
            end_x = star.x + max(0.1, star.speed * self.delta_time * star_blur_length)
            try:
                 pygame.draw.aaline(screen, WHITE, (star.x, star.y), (end_x, star.y))
            except TypeError: 
                 pygame.draw.line(screen, WHITE, (int(star.x), int(star.y)), (int(end_x), int(star.y)))
        current_y = self.scroll_pos[1]
        for i, line in enumerate(self.info_text):
            if self.font:
                try:
                    text_surface = self.font.render(line, True, self.text_color)
                    screen.blit(text_surface, (int(self.scroll_pos[0]), int(current_y)))
                except pygame.error as e:
                    print(f"Error rendering text line '{line}': {e}")
                except Exception as e: 
                     print(f"Unexpected error rendering text: {e}")
            current_y += self.line_height

        logo_y  = current_y + 10 
        start_x = self.scroll_pos[0] + 50
        if self.images:
             img_order = ['python', 'pygame', 'box2d'] 
             current_logo_x = start_x
             for key in img_order:
                 if key in self.images and self.images[key]: 
                      try:
                           screen.blit(self.images[key], (int(current_logo_x), int(logo_y)))
                           current_logo_x += self.images[key].get_width() + 10
                      except Exception as e:
                           print(f"Error drawing logo '{key}': {e}")