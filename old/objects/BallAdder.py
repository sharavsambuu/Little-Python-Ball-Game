# -*- coding: utf-8 -*-
from GameObject import *
from Vector2 import Vector2
from Ball import *
from Box2D import *

class BallAdder(GameObject):
    game = None
    nextBallpos = None
    nextBallType = None
    diffuculty = 0
    clock = None
    def __init__(self,  gameState):
        self.game = gameState
        self.nextBallpos = (randint(tile_size/2, (tile_dim[0]-1)*tile_size),(tile_dim[1]-2)*tile_size-0.8)
        self.nextBallType = randint(0,5)
        self.clock = 0.
    def update(self, timeDelta):
        self.clock += timeDelta/1000.
        if self.clock>=5:
            self.clock = 0.
            for iter in range(0,3):
                # бөмбөг нэмэх
                bullet = Ball(self.game,self.game.world, self.nextBallpos, self.nextBallType)
                bullet.firstThump = False
                self.game.objects.append(bullet)
                self.nextBallpos = (randint(tile_size/2, (tile_dim[0]-1)*tile_size),(tile_dim[1]-2)*tile_size-0.8)
                self.nextBallType = randint(0,5)            
        pass
    