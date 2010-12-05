# coding: utf-8
import pygame
from State import *
from Settings import *
from random import randint

class Star(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

class About(State):    
    pos = None
    textSpeed = None 
    str = None
    color = None
    count = 0
    images = None
    stars = []
    def __init__(self):
        State.__init__(self)
        
        self.images = self.load_image(['data/image/logo/box2d.png',
                                  'data/image/logo/eclipse.png',
                                  'data/image/logo/pygame.gif',
                                  'data/image/logo/python.png'])
        self.font = pygame.font.Font("data/font/fsex2p00_public.ttf", 16)
        self.pos = [screen_size[0]/4, screen_size[1]]
        self.speed = 10
        self.color = (255,255,255)
        
        self.str =(
               u"                    Тоглоомын тухай",
               u"",
               u"     Ашигласан хэл : Python - http://www.python.org",
               u"     Ашигласан сан : PyGame - http://www.pygame.org",
               u"                   PyBox2d - http://pybox2d.blogspot.com,",
               u"                            http://www.box2d.org",
               u"     Ашигласан IDE : Eclipse + PyDev",
               u"     Ашигласан хөгжим : CrayonBall-ийн авианууд,",
               u"                        http://www.8bc.org оос авсан хөгжимүүд",
               u"",
               u"     Хөгжүүлэгчид :",
               u"           Б.Пунцагбалжир - nomadx88@gmail.com",
               u"                           http://nomadx88.blogspot.com",
               u"           Г.Шаравсамбуу - sharavsambuu@gmail.com",
               u"                          http://sharavaa.blogspot.com",
               u"",
               u"     Компютер тоглоомыг зураачид програмистууд хөгжим зохиогчид", 
               u"     дезайнерууд гээд л тал бүрийн чадвартай хүмүүс нийлэн байж", 
               u"     бүтээдэг. Одоогоор Cyber Boyz Games маань хоёрхон гишүүнтэй", 
               u"     байгаа бөгөөд хоёулаа програмчилж л чадна. Харин бусад пиксел", 
               u"     арт, спрайт шиитүүдээс өгсүүлээд артистуудын хийдэг зүйлсээр", 
               u"     их дутагдаж байна. Хэрвээ та энэ талын сонирхолтой бол мөн", 
               u"     компютер тоглоом хийх мөрөөдөлтэй бол бидэнтэй холбоо бариарай.", 
               u"     Бид юу юуны тухайнд яаралгүйгээр эхний ээлжинд хэд хэдэн", 
               u"     тоглоомуудыг зүгээр л үнэгүй байхаар хийж үзэх бодолтой байна.",
               u"     Харин цаашид хөөрхөн тоглоом хийчихдэг хөгжүүлэлт тал дээр нэг", 
               u"     нэгнээ нөхсөн боломжийн баг бүрдвэл бид андройд iphone-оос", 
               u"     өгсүүлээд PC болон консолиуд хүртлэх бусад зах зээлүүдэд", 
               u"     тоглоом бичиж гаргадаг болохыг үгүйсгэх аргагүй ээ. Хэрвээ тэгсэн",
               u"     тохиолдолд индие студи байгуулаад ажилласанч болох л юм.",
               u"     Санал бодлоо email-ээр солилцоцгооё! Мөн асуух зүйл байвал", 
               u"     чадахынхаа хэрээр хариулахад бэлэн шүү.",
               u"",
               u"",
               u"                Cyber Boyz Games team",
               u"          http://cyberboyzgames.blogspot.com",
               u"",
               u"",
               u"",
               u"      Powered by:")
        
        pygame.mixer_music.load("data/sound/music/song12.ogg")
        
        for n in xrange(200):
            x = float(randint(0, screen_size[0]))
            y = float(randint(0, screen_size[1]))
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
    
    def handle_update(self, timeDelta):
        self.timeDelta = timeDelta
        self.pos[1] -= timeDelta/1000.*self.speed
        if self.pos[1]+self.count*16+60<0:
            self.pos[1]=screen_size[1]
        
        y = float(randint(0, screen_size[0]-1))
        speed = float(randint(10, screen_size[1]))
        star = Star(screen_size[0], y, speed)
        self.stars.append(star)        
        pass
    
    def handle_erase(self, screen):
        screen.fill((0,0,0))
        
    def handle_draw(self, screen):
        # Оддыг зурах
        for star in self.stars:
            new_x = star.x-self.timeDelta/1000.*star.speed
            pygame.draw.aaline(screen, self.white, (new_x, star.y), (star.x+1., star.y))
            star.x = new_x
        def on_screen(star):
            return star.x > 0
        # үзэгдэхгүй оддыг хасна
        stars = filter(on_screen, self.stars)
                
        self.count = 0
        for iter in self.str:
            try:
                text = self.font.render(iter, True, self.color)                
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
        #eclipse
        screen.blit(self.images[1],(self.pos[0]+50+60+200+76,self.pos[1]+self.count*15))
        pass
    
    def load_image(self, image):
        if type(image) is list:
            return map(self.load_image, image)
        elif type(image) is str:  
            return pygame.image.load(image).convert_alpha()