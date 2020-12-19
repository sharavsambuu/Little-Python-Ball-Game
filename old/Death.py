# coding: utf-8
from State import State
import pygame
import Box2D as box2d

class Death(State):
    
    velocityIterations = 10
    positionIterations = 8
    gravity = (0, 20)
    doSleep = True
    pixels_per_unit = 48
    
    def __init__(self):
        worldAABB=box2d.b2AABB()
        worldAABB.lowerBound = (-8, -8)
        worldAABB.upperBound = (30, 30)
        
        self.world = box2d.b2World(worldAABB, self.gravity, self.doSleep)        
        
        floor_bodyDef = box2d.b2BodyDef()
        floor_bodyDef.position = (14, 8)
        floor_bodyDef.userData = self
        floor_body = self.world.CreateBody(floor_bodyDef)
        floor_shapeDef = box2d.b2PolygonDef()
        floor_shapeDef.SetAsBox(16, 1)
        floor_body.CreateShape(floor_shapeDef)
        
    def handle_enter(self, parameters):
        self.next_state = parameters['next_state']
        self.next_state_parameters = parameters.setdefault('parameters', {})
        self.next_state_parameters={'totalScore':parameters['totalScore'],'edit':parameters['edit']}
        
        self.delay = parameters.setdefault('delay', 2000)
        self.time_passed = 0
        self.background = None
        self.shader = None
        self.screenFont = pygame.font.Font("data/font/fsex2p00_public.ttf", 70)
        text = u"Тоглоом дууслаа"
        self.message = self.screenFont.render(text, True, (255,255,255))
                
        bodyDef = box2d.b2BodyDef()
        bodyDef.position = (8, -2)
        bodyDef.angle = -0.5
        bodyDef.userData = self
        self.message_body = self.world.CreateBody(bodyDef)
        shapeDef = box2d.b2PolygonDef()
        shapeDef.density = 0.5
        shapeDef.friction = 0.95
        shapeDef.restitution = 0.5
        shapeDef.SetAsBox(self.message.get_width()/2.0/self.pixels_per_unit, 
                          self.message.get_height()/2.0/self.pixels_per_unit)
        self.message_body.CreateShape(shapeDef)
        self.message_body.SetMassFromShapes()
        self.message_body.SetLinearVelocity = box2d.b2Vec2(100.0,0)
        
        
    def handle_exit(self):
        self.world.DestroyBody(self.message_body)
        self.background = None
        
    def handle_key_down(self, key):
        pass
    
    def handle_key_up(self, key):
        pass
        
    def handle_mouse_button_down(self, button, position):
        pass
    
    def handle_mouse_button_up(self, button, position):
        pass
    
    def handle_mouse_motion(self, relative, position, buttons):
        pass
        
    def handle_update(self, timeDelta):
        self.world.Step(timeDelta/1000.0, self.velocityIterations, self.positionIterations)
        self.time_passed += timeDelta
        if self.delay <= self.time_passed:
          self.engine.change_state(self.next_state, self.next_state_parameters)
    
    def handle_erase(self, screen):
        if not self.background:
          self.background = screen.copy()        
        screen.blit(self.background, (0,0))
        
    def handle_draw(self, screen):
        if not self.shader:
          self.shader = pygame.Surface(screen.get_size())
          self.shader.fill((0,0,0))
        alpha = min(255 , 255*self.time_passed/self.delay)
        alpha = alpha if alpha != 128 else 129
        self.shader.set_alpha(alpha)
        screen.blit(self.shader, (0,0))
        angle = int(self.message_body.angle*180/3.14)
        rotated = pygame.transform.rotate(self.message, -angle)
        pos = self.message_body.GetPosition()
        x = int(pos.x*self.pixels_per_unit - rotated.get_width()/2)
        y = int(pos.y*self.pixels_per_unit - rotated.get_height()/2)
        screen.blit(rotated, (x, y))
    
