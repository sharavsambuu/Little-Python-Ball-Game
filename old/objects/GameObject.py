# -*- coding: utf-8 -*-
import Box2D as box2d
from Settings import *
from random import random
from math import *
from copy import deepcopy as copy
import pygame

MAGIC_PINK = (255,0,255)
def load_image_with_color_key(filename):
    image = pygame.image.load(filename)
    image_ck = pygame.Surface(image.get_size())
    image_ck.fill(MAGIC_PINK)  
    image_ck.blit(image, (0,0))
    image_ck = image_ck.convert()
    image_ck.set_alpha(None)
    image_ck.set_colorkey(MAGIC_PINK)
    return image_ck

def load_image(image):
    if type(image) is list:
        return map(load_image, image)
    elif type(image) is str:  
        return pygame.image.load(image).convert_alpha()
  
class GameObject(object):
    def addCollision(self, point, other):
        """шинэ физик мөргөлдөөнүүдийг барьж авах"""
        pass
    
    def removeCollision(self, point, other):
        """салж байгаа физик мөргөлдөөнийг барьж авах"""
        pass
    
    def addPersis(self, point, other):
        pass
    
    def update(self, timeDelta):
        """объектийн төлөвүүдийг шинэчлэх"""
        pass
        
    def draw( self, surface):
        """өгөгдсөн surface дээр объектийн мэдээллийг зурах"""
        pass
            
class Dynamic:
    pass

class Static:
    pass

