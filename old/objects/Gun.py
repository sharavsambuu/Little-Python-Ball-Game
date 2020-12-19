# -*- coding: utf-8 -*-
from GameObject import *

class Gun(GameObject):
    image = load_image('data/image/gun.png')
        
    def __init__(self, world, startPos):
        self.world = world
        bodyDef = box2d.b2BodyDef()
        bodyDef.position = (startPos[0]/tile_size,startPos[1]/tile_size)
        bodyDef.userData = self
        self.body = self.world.CreateBody(bodyDef)
        shapeDef = box2d.b2PolygonDef()
        shapeDef.setVertices([(-0.5833,-0.4375),
                              (0.5833,-0.4375),
                              (-0.270833,0.25),
                              (-0.5833,0.25)])
        #28 - 0.5833
        #21 - 0.4375
        #13 - 0.270833
        #12 - 0.25
        shapeDef.density = 0.5
        shapeDef.friction = 0.95        
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()        
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
