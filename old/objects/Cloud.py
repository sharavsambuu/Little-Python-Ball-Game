# -*- coding: utf-8 -*-
from GameObject import *
from Vector2 import Vector2
from Ball import *
from random import randint

class Cloud(GameObject):
    image = load_image('data/image/cloud/cloud.png')
    pos = None
    speed = None
    def __init__(self, startPos):
        self.pos = startPos
        self.speed = randint(5,15)
    
    def update(self, timeDelta):
        self.pos[0] -=  self.speed * timeDelta/1000.
        if self.pos[0]+self.image.get_width()<=0:
            self.pos = [screen_size[0], randint(0, screen_size[1]-self.image.get_height()/2.)]
            self.speed = randint(5,15)
            pass
        pass
        
    def draw( self, surface):
        surface.blit(self.image, (int(self.pos[0]),int(self.pos[1])))
        pass