# coding: utf-8
from Engine import *
from Settings import *
from Menu import *
from Game import *
from Win import *
from Death import *
from Score import *
from About import *

import pygame
pygame.mixer.init(44100, 16, 2, 1024)
pygame.init()

first_state = 'menu'

first_state_parameters = {}
states = {'menu' : Menu([(u"Эргэж орох", 'game', {'new': False}),
                         (u"Тоглоом эхлүүлэх", 'game', {'new': True}),
                         (u"Оноо",'score',{'totalScore':0,'edit':False}),                         
                         (u"Тохиргоо", [( u"fps", (False, True)),
                                        ( u"Хөгжим", (True, False))]),
                         (u"Тухай",'about',{}),                         
                         (u"Гарах", Menu.MENU_QUIT) ]),
          'game' : Game(),
          'win'  : Win(),
          'death': Death(),
          'score': Score(),
          'about': About()}

if __name__ == '__main__':
    try:
        game = Engine(states, 
              first_state, 
              first_state_parameters, 
              screen_size,
              window_title=u"Cyber Boyz Games - Little PyBall Game")
        game.run()
    except:
        pass
