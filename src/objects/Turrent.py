# -*- coding: utf-8 -*-
from GameObject import *
from Vector2 import Vector2
from Ball import *
from Box2D import *

class Turrent(GameObject):
    game = None
    image = load_image('data/image/turrent/turrent.png')
    images = load_image(['data/image/ball/yellow_ball.png',
                         'data/image/ball/red_ball.png',
                         'data/image/ball/orange_ball.png',
                         'data/image/ball/green_ball.png',
                         'data/image/ball/black_ball.png',
                         'data/image/ball/blue_ball.png'])
    pos = None
    rotation_direction = 0.
    #rotation_speed = 360. # секундэд нэг градус
    #rotation_speed = 180. # секундэд 0.5 градус
    rotation_speed = 45.
    sprite_rotation = 0.
    is_shoot = False
    nextBallType = None
    def __init__(self,  gameState, startPos):
        self.game = gameState
        self.pos = startPos
        self.nextBallType = randint(0,5)
    def update(self, timeDelta):
        rotation_direction = pygame.mouse.get_rel()[0]/3.
        self.sprite_rotation -= rotation_direction*self.rotation_speed*timeDelta/3000.
        if self.sprite_rotation<-90.:
            self.sprite_rotation=-90.
        elif self.sprite_rotation>90.:
            self.sprite_rotation=90.
        dir_vec_x = sin(self.sprite_rotation*pi/180.)
        dir_vec_y = cos(self.sprite_rotation*pi/180.)
        direction = b2Vec2(-dir_vec_x, -dir_vec_y) 
        # бөмбөгөөр буудах
        if self.is_shoot:
            bullet = Ball(self.game,self.game.world, (self.pos[0],self.pos[1]-0.8), self.nextBallType)
            bullet.body.SetLinearVelocity(direction*20)
            self.game.objects.append(bullet)
            self.nextBallType = randint(0,5)
            self.is_shoot=False
            pass
        
    def draw( self, surface):
        surface.blit(self.images[self.nextBallType],self.pos)
        rotated_sprite = pygame.transform.rotate(self.image,self.sprite_rotation)
        rotation_offset_x = (rotated_sprite.get_width()-self.image.get_width())/2
        rotation_offset_y = (rotated_sprite.get_height()-self.image.get_height())/2
        surface.blit(rotated_sprite, (int(self.pos[0])-rotation_offset_x,
                                      int(self.pos[1])-rotation_offset_y))
        pass