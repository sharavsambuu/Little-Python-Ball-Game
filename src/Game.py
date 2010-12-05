# coding: utf-8

import pygame
from sys import *
from pygame import *
import Box2D as box2d
from State import *
from Settings import *
from objects import *

from random import randint

class Game(State):
    engine = None
    velocityIterations = 10
    positionIterations = 8
    gravity = (0, -9.81)
    doSleep = True
    objects = []
    turrent = None
    clouds = []
    
    point = 0
    ballTotal = 210
    ballCount = 0
    ballPercent = 0
    
    def __init__(self):
        State.__init__(self)
        worldAABB=box2d.b2AABB()
        worldAABB.lowerBound = (-50/tile_size, -50/tile_size)
        worldAABB.upperBound = ((screen_size[0]+50)/tile_size, (screen_size[1]+50)/tile_size)

        self.world = box2d.b2World(worldAABB, self.gravity, self.doSleep)
        self.listener = MyContactListener(self.engine)
        self.world.SetContactListener(self.listener)       
        
        # дуу авианууд
        self.ploop = pygame.mixer.Sound('data/sound/fx/ploop.wav')        
            
        self.window_title = u"Little PyBall"
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True) # курсорыг фрэймээс гарахгүй болгоно
        
        self.font = pygame.font.Font("./data/font/fsex2p00_public.ttf", 35)
                
        self.addObjects()
        
        self.pause = False

        
    def handle_enter(self, parameters):
        if parameters['new']:
            pygame.mixer_music.load("data/sound/music/song12.ogg")
            #pygame.mixer_music.load("data/sound/music/DikkiPainguinLoop(rev-1).ogg")
            pygame.mixer_music.play(-1)
            self.reset()
        else:
            self.pause = False            
        if parameters[u"Хөгжим"]:
            pygame.mixer_music.play(-1)
        else:
            pygame.mixer_music.stop()
        pass
            
    def handle_exit(self):
        pygame.mixer.music.stop()
        #self.objects = []
        #self.clouds = []        
        
    def handle_key_down(self, key):
        if key==KEY_RIGHT:
            pass
        elif key==KEY_LEFT:
            pass
        elif key==KEY_JUMP:
            pass
        elif key==KEY_SPECIAL:
            pass
        elif key==KEY_SHOOTBALL:
            pass
        elif key==KEY_QUIT:
            self.engine.change_state('menu')            
    
    def handle_key_up(self, key):
        if key==KEY_RIGHT:
            self.ploop.play()
            pass
        elif key==KEY_LEFT:
            pass
        elif key==KEY_JUMP:
            pass
        elif key==KEY_SHOOTBALL:
            pass
            
    def handle_mouse_button_down(self, button, position):
        if pygame.mouse.get_pressed()[0]:
            self.turrent.is_shoot=True
        pass
    
    def handle_mouse_button_up(self, button, position):
        
        pass
    
    def handle_mouse_motion(self, relative, position, buttons):
        pass
    # тоглоомд оролцох объектүүдийг шинэчлэнэ мөн физик итерацийг хийнэ
    def handle_update(self, timeDelta):
        if not self.pause:
            self.world.Step(timeDelta/1000.0, self.velocityIterations, self.positionIterations)
            self.turrent.update(timeDelta)
            self.ballAdder.update(timeDelta)
            for obj in self.objects:
                obj.update(timeDelta)
                if isinstance(obj, Ball) and  obj is not None:
                    if not obj.isTraversed:
                        obj.val = obj.recursive_count()
                        if obj.val>=4:
                            obj.recursDel()
                            self.ploop.play()
                            self.combo.ploop()
                            self.point += obj.val-3             
            self.ballCount = 0
            for obj in self.objects:
                if isinstance(obj, Ball):
                    self.ballCount += 1
                    obj.isTraversed = False
                    if obj.alive==False:
                        obj.deleteYourself()                     
                        self.objects.remove(obj)
                        pass
            for cloud in self.clouds:
                cloud.update(timeDelta)
            
            self.ballPercent = int((self.ballCount*100)/self.ballTotal)
            if self.ballPercent>100:
                self.ballPercent = 100
                self.engine.states['menu'].resume = False
                self.engine.change_state('death', {'next_state': 'score','totalScore':self.point,'edit':True})
            self.percentFrame.update(timeDelta)
            
            self.combo.update(timeDelta)                              
                    
    def handle_erase(self, screen):
        screen.fill((0,0,250))
        
    # тоглоомд оролцох бүх объектүүдийг зурна
    def handle_draw(self, screen):
        for cloud in self.clouds:
            cloud.draw(screen)
        for obj in self.objects:
            obj.draw(screen)
        self.turrent.draw(screen)
        
        self.percentFrame.draw(screen)
        str1 = u"оноо: %d"%self.point
        str2 = u"%d"%self.ballPercent
        try:
            text = self.font.render(str1, True, (0,0,0))
            screen.blit(text, ((tile_dim[0]+1)*tile_size+tile_size/2,tile_size*3))
            text = self.font.render(str2, True, (255,255,255))
            screen.blit(text, ((tile_dim[0]+2)*tile_size+4,tile_size*9))
        except error:
            pass        
        
    def addObjects(self):
        # дээд хүрээ
        for i in range(0,tile_dim[0]):
            self.objects.append(StaticBox(self.world, (i*tile_size,0-tile_size/2.)))
        # доод хүрээ
        for i in range(0,tile_dim[0]):
            self.objects.append(StaticBox(self.world, (i*tile_size,(tile_dim[1]-1)*tile_size+tile_size/2.)))            
        # зүүн хүрээ
        for i in range(1,tile_dim[1]):
            self.objects.append(StaticBox(self.world, (0-tile_size/2.,i*tile_size-tile_size/2.)))
            pass
        # баруун хүрээ
        for i in range(1,tile_dim[1]):
            self.objects.append(StaticBox(self.world, ((tile_dim[0]-1)*tile_size+tile_size/2.,i*tile_size-tile_size/2.)))
            pass        
        # бөмбөлөгнүүдийг нэмэх
        for iter in range(0,60):
            self.objects.append(Ball(self, self.world, (randint(tile_size/2, (tile_dim[0]-1)*tile_size-tile_size/2),
                                                        randint(tile_size/2, (tile_dim[1]-1)*tile_size-tile_size/2)),
                                                        randint(0,5)))
            pass
        # үүлсийг нэмэх
        for iter in range(0,10):
            self.clouds.append(Cloud([randint(0,screen_size[0]), randint(0,screen_size[1])]))            
        # Буудах зориулалттай
        self.turrent = Turrent(self, ((tile_dim[0]-1)/2*tile_size+tile_size/2.,
                                      (tile_dim[1]-1)*tile_size-tile_size/2.))
        self.ballAdder = BallAdder(self)
        
        # хувь харуулах зориулалттай
        self.percentFrame = ShowFilledPercent(self, ((tile_dim[0]+2)*tile_size,tile_size*5))
        
        self.combo = ComboAdder(self)
        
        
    def reset(self):
        self.pause = True
        for obj in self.objects:
            if isinstance(obj, Ball):
                obj.deleteYourself()                     
                self.objects.remove(obj)
        self.point = 0
        # бөмбөлөгнүүдийг нэмэх
        for iter in range(0,60):
            self.objects.append(Ball(self, self.world, (randint(tile_size/2, (tile_dim[0]-1)*tile_size-tile_size/2),
                                                        randint(tile_size/2, (tile_dim[1]-1)*tile_size-tile_size/2)),
                                                        randint(0,5)))
            pass
        self.pause = False        
        pass
        
        
class MyContactListener(box2d.b2ContactListener):
    def __init__(self, engine): 
        super(MyContactListener, self).__init__() 
        self.engine = engine
        self.new = [] # мөргөлдсөн дүрснүүдийн олонлог
        self.persisted = [] # шүргэлцсэн байдалтай байгаа дүрснүүдийн олонлог
        self.removed = [] # мөргөлдөөд салж байгаа дүрснүүдийн олонлог
    
    def getAdd(self):
        return self.new
        self.new = []
        
    def getPersist(self):
        return self.persisted
        self.persisted = []
        
    def getRemove(self):
        return self.removed
        self.removed = []
        
    def Add(self, point):
        """Мөргөлдөөнийг барих"""
        obj1 = point.shape1.GetBody().GetUserData()
        obj2 = point.shape2.GetBody().GetUserData()
        obj1.addCollision(point, obj2)
        obj2.addCollision(point, obj1)
        pass
         
    def Persist(self, point):
        """шүргэлдээнийг барих =D"""
        pass
        
    def Remove(self, point):
        """салалдааныг барих XD"""
        obj1 = point.shape1.GetBody().GetUserData()
        obj2 = point.shape2.GetBody().GetUserData()
        obj1.removeCollision(point, obj2)
        obj2.removeCollision(point, obj1)
            
    def Result(self, point):
        """үр дүн"""
        pass