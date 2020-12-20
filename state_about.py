from random import randint
import pygame
from state    import *
from settings import *

class Star(object):
    def __init__(self, x, y, speed):
        self.x     = x
        self.y     = y
        self.speed = speed

class About(State):
    pos        = None
    text_speed = None
    string     = None
    color      = None
    count      = 0
    images     = None
    stars      = []
    def __init__(self):
        State.__init__(self)
        self.images = self.load_image(['data/image/logo/box2d.png'  ,
                                       'data/image/logo/eclipse.png',
                                       'data/image/logo/pygame.gif' ,
                                       'data/image/logo/python.png'])
        self.font  = pygame.font.Font("data/font/fsex2p00_public.ttf", 16)
        self.pos   = [screen_size[0]/4, screen_size[1]]
        self.speed = 10
        self.color = (255,255,255)

        self.string = (
                "         About the game",
                "",
                "    Programming language : Python",
                "    Rendering library    : PyGame",
                "    Physics library      : PyBox2d",
                "    Music                : taken from CrayonBall",
                "",
                "    Developer : sharavsambuu@gmail.com",
                "                http://sharavaa.blogspot.com",
                "",
                "",
                "",
                "      Powered by:"
                )

        pygame.mixer_music.load("data/sound/music/song12.ogg")

        for n in range(200):
            x     = float(randint(0, screen_size[0]))
            y     = float(randint(0, screen_size[1]))
            speed = float(randint(10, 300))
            self.stars.append(Star(x, y, speed))
        self.white = (255, 255, 255)
        pass

    def handle_enter(self, parameters):
        pygame.mixer_music.play(-1)
        pass

    def handle_exit(self):
        pygame.mixer_music.stop()
        pass

    def handle_key_down(self, key):
        if key==KEY_QUIT or key==pygame.K_RETURN or key==pygame.K_LEFT or key == pygame.K_BACKSPACE:
            pygame.mixer_music.stop()
            self.engine.change_state('menu')

    def handle_update(self, delta_time):
        self.delta_time = delta_time
        self.pos[1]    -= delta_time/1000.*self.speed
        if self.pos[1]+self.count*16+60<0:
            self.pos[1] = screen_size[1]
        y     = float(randint( 0, screen_size[0]-1))
        speed = float(randint(10, screen_size[1]))
        star  = Star(screen_size[0], y, speed)
        self.stars.append(star)
        pass

    def handle_erase(self, screen):
        screen.fill((0,0,0))

    def handle_draw(self, screen):
        # Оддыг зурах
        for star in self.stars:
            new_x  = star.x-self.delta_time/1000.*star.speed
            pygame.draw.aaline(screen, self.white, (new_x, star.y), (star.x+1., star.y))
            star.x = new_x
        def on_screen(star):
            return star.x > 0
        # үзэгдэхгүй оддыг хасах
        stars = filter(on_screen, self.stars)
        self.count = 0
        for el in self.string:
            try:
                text = self.font.render(el, True, self.color)
                screen.blit(text, (self.pos[0],self.pos[1]+self.count*15))
            except error:
                pass
            self.count += 1
        #python
        screen.blit(self.images[3],(self.pos[0]+50,self.pos[1]+self.count*15))
        #pygame
        screen.blit(self.images[2],(self.pos[0]+50+60,self.pos[1]+self.count*15))
        #box2d
        screen.blit(self.images[0],(self.pos[0]+50+60+200,self.pos[1]+self.count*15))
        pass

    def load_image(self, image):
        if type(image) is list:
            return list(map(self.load_image, image))
        elif type(image) is str:
            return pygame.image.load(image).convert_alpha()
