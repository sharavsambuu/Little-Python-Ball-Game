# -*- coding: utf-8 -*-
from GameObject import *
from Vector2 import Vector2
from Ball import *
from Box2D import *

class ShowFilledPercent(GameObject):
    game = None
    pos = None
    pos1 = (0,0)
    dimension = (65,400)
    dim = 0
    percent = 0
    def __init__(self, gameState, startPos):
        self.game = gameState
        self.pos = startPos        
    
    def update(self, timeDelta):
        self.dim = int((self.game.ballPercent*self.dimension[1])/100)
        self.pos1 = (self.pos[0],self.pos[1]+self.dimension[1]-self.dim)
        pass       
        
    def draw( self, surface):
        # хүрээгий нь зурж эхлэх
        color = (200,200,200)
        pygame.draw.rect(surface, color, Rect(self.pos,self.dimension))
        # дүүргэлтийг нь харуулах
        color = (0,0,0)
        pygame.draw.rect(surface, color, Rect(self.pos1,(self.dimension[0],self.dim)))
        pass
        