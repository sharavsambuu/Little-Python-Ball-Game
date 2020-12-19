# coding: utf-8
from Settings import *
from GameObject import *
from random import randint
import math
from warnings import catch_warnings

class Ball(GameObject):
    image = None
    images = load_image(['data/image/ball/yellow_ball.png',
                         'data/image/ball/red_ball.png',
                         'data/image/ball/orange_ball.png',
                         'data/image/ball/green_ball.png',
                         'data/image/ball/black_ball.png',
                         'data/image/ball/blue_ball.png'])
    body = None
    shoot = False    
    pos = [0,0]
    type = 0    
    collided_objects = None
    collided_count = None
    isTraversed = False
    state = None
    val = 0
    firstThump = True # мөргөх авиа гаргахад хэрэглэнэ
    
    def __init__(self, state, world, startPos, t):
        self.world = world
        self.state = state        
        bodyDef = box2d.b2BodyDef()
        bodyDef.position = (startPos[0]/tile_size,startPos[1]/tile_size)
        bodyDef.userData = self
        self.body = self.world.CreateBody(bodyDef)
        shapeDef = box2d.b2CircleDef()
        shapeDef.radius = 0.5
        shapeDef.density = 1
        shapeDef.friction = 0.2
        shapeDef.restitution = 0.1
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()        
        self.start = box2d.b2Vec2(self.body.GetPosition())
        self.type = t
        self.image = self.images[self.type]
        self.collided_objects = []
        self.alive = True
        self.collided_count = 1
        
        self.font = pygame.font.Font("data/font/fsex2p00_public.ttf", 15)
                        
        self.thump = pygame.mixer.Sound('data/sound/fx/thump.ogg')
    
    def recursive_count(self):
        self.isTraversed = True
        sum = 0
        for iter in self.collided_objects:
            if not iter.isTraversed:
                sum+=iter.recursive_count()        
        return sum+1
    
    def recursDel(self):
        self.alive = False
        for iter in self.collided_objects:
            if iter.alive:
                iter.recursDel()                  
    
    def deleteYourself(self):        
        self.world.DestroyBody(self.body)
        self.collided_objs = []
        self.images = []
        del self.body           
    
    def update(self, timeDelta):
        if not self.alive:
            return  

    def draw( self, surface):
        if not self.alive:
            return
        self.pos = [self.body.GetPosition().x,self.body.GetPosition().y]
        rotated = pygame.transform.rotate(self.image, -self.body.angle*180/3.14)
        rotation_offset_x = (rotated.get_width()-self.image.get_width())/2
        rotation_offset_y = (rotated.get_height()-self.image.get_height())/2
        surface.blit(rotated, (int(self.pos[0]*tile_size)-rotation_offset_x,
                               int(self.pos[1]*tile_size)-rotation_offset_y))        
        self.collided_count=0        
        for iter in self.collided_objects:
            pygame.draw.line(surface, 
                             (0,0,0), # хар өнгийн шугам
                             (self.pos[0]*tile_size+tile_size/2,self.pos[1]*tile_size+tile_size/2),
                             (iter.pos[0]*tile_size+tile_size/2,iter.pos[1]*tile_size+tile_size/2))
            self.collided_count += 1
        #str = "%d-%d "%(self.type,self.val)
        #try:
            #text = self.font.render(str, True, (255,10,10))
            #surface.blit(text, (self.pos[0]*tile_size+tile_size/2,
                            #self.pos[1]*tile_size+tile_size/2))
        #except error:
            pass        
    
    def addCollision(self, point, other):
        """шинэ физик мөргөлдөөнүүдийг барьж авах"""
        if isinstance(other, Ball) and other.type==self.type:
            if not other in self.collided_objects:
                self.collided_objects.append(other)
        if self.firstThump:
            self.thump.play()
            self.firstThump=False
    
    def removeCollision(self, point, other):
        """салж байгаа физик мөргөлдөөнийг барьж авах"""
        if isinstance(other, Ball) and other.type==self.type:
            if other in self.collided_objects:
                self.collided_objects.remove(other)
    
    def addPersist(self, point, other):
        pass

    