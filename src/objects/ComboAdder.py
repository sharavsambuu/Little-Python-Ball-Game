import pygame

class ComboAdder(object):
    
    dt = None
    comboCount = None
    game = None
    def __init__(self, state):
        self.dt = 0.
        self.comboCount = 0
        self.game = state
        self.boom = pygame.mixer.Sound('data/sound/fx/boom.ogg')
        pass
    def update(self, deltaTime):
        self.dt += deltaTime/1000.
        pass
    def ploop(self):
        if self.dt<2.5:
            self.comboCount += 1
        else:
            self.comboCount = 0
            
        if self.comboCount>2:
            self.game.point += 4
            self.boom.play()
            pass
        
        self.dt = 0.
        pass
    pass