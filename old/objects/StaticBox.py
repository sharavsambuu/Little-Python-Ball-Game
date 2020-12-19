# -*- coding: utf-8 -*-
from GameObject import *

class StaticBox(GameObject):
    image = load_image('data/image/box/box.png')
    #image = load_image('data/image/gun.png')
    def __init__(self, world, startPos):
        self.world = world
        bodyDef = box2d.b2BodyDef()
        bodyDef.position = (startPos[0]/tile_size,startPos[1]/tile_size)
        bodyDef.userData = self
        self.body = self.world.CreateBody(bodyDef)
        shapeDef = box2d.b2PolygonDef()
        shapeDef.density = 0.5
        shapeDef.friction = 0.95
        shapeDef.SetAsBox(0.5, 0.5)
        self.body.CreateShape(shapeDef)
        #self.body.SetMassFromShapes()
        # массийг 0 болгосноор статик физик бие үүснэ
        self.rotated = self.image
        
        self.alive = True
        
    def draw( self, surface):
        if not self.alive:
            return
        pos = self.body.GetPosition()
        angle = int(self.body.angle*180/3.14)
        self.rotated = pygame.transform.rotate(self.image, -angle)        
        rotation_offset_x = (self.rotated.get_width() - self.image.get_width())/2
        rotation_offset_y = (self.rotated.get_height() - self.image.get_height())/2
        surface.blit(self.rotated, (int(pos.x*tile_size)-rotation_offset_x, 
                                    int(pos.y*tile_size)-rotation_offset_y))  
        
    def addPersist(self, point, other):
        pass      
