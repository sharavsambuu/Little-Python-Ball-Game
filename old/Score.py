# coding: utf-8
from State import *
from Settings import *
import pygame

class Score(State):
    list = []
    name = None
    def __init__(self):
        State.__init__(self)
        self.font = pygame.font.Font("data/font/fsex2p00_public.ttf", 35)
        self.pos = [screen_size[0]/4, screen_size[1]/4]
        self.timer = 0.
        pass
    
    def handle_enter(self, parameters):
        self.edit = parameters['edit'] 
        self.list = []
        f = open('data/score/score','r')
        for iter in range(0,10):
            line = f.readline()            
            if line.split()[1].__eq__("-"):
                self.list.append([line.split()[0],0])
            else:
                self.list.append([line.split()[0],int(float(line.split()[1]))])
        f.close()
        self.name = u"-"
        if parameters['edit']:
            self.name = u"-"                        
            self.player = [self.name,parameters['totalScore']]
            self.list.append(self.player)
            self.sortByScore(self.list)
        pass
    
    def handle_exit(self):
        if self.edit:
            l = self.name.split()
            self.name=""
            for i in l:
                self.name+=i
            if len(self.name)>10:
                self.name = self.name[0:11]
            if len(self.name)==0:
                self.name = "-"    
            f = open('data/score/score','w')        
            for iter in range(0,10):
                line = self.list[iter][0]+" "+str(self.list[iter][1])+"\n"
                f.write(line)            
            f.close()        
        pass
            
    def handle_key_down(self, key):
        if key==KEY_QUIT or key==pygame.K_RETURN or key==pygame.K_LEFT:
            self.engine.change_state('menu')
        elif key == pygame.K_BACKSPACE:
            if self.edit:
                self.name = self.name[0:len(self.name)-1]
                if len(self.name)==0:
                    self.name=u"-"
                self.player[0] = self.name
        else:
            if self.edit:
                if self.name.__eq__("-"):
                    self.name=""
                if not len(self.name)>11:
                    keys = pygame.key.get_pressed()
                    for key_constant, pressed in enumerate(keys):
                        if pressed:
                            key_name = pygame.key.name(key_constant)
                            if not (key_name.__eq__("numlock") or 
                                    key_name.__eq__("space") or
                                    key_name.__eq__("caps lock") or
                                    key_name.__eq__("menu") or
                                    key_name.__eq__("left meta") or
                                    key_name.__eq__("left shift") or
                                    key_name.__eq__("right shift") or
                                    key_name.__eq__("left alt") or
                                    key_name.__eq__("right alt") or
                                    key_name.__eq__("left ctrl") or
                                    key_name.__eq__("right ctrl") or
                                    key_name.__eq__("end") or
                                    key_name.__eq__("home") or
                                    key_name.__eq__("insert") or
                                    key_name.__eq__("delete") or
                                    key_name.__eq__("tab") or
                                    key_name.__eq__("page up") or
                                    key_name.__eq__("page down") or
                                    key_name.__eq__("backspace")):
                                if self.timer>0.05:
                                    self.name += str(key_name)
                                    self.timer = 0.                                 
                    self.player[0] = self.name
                else:
                    self.name = self.name[0:11]                                                                              
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
        self.timer += timeDelta/1000.
        pass
    
    def handle_erase(self, screen):
        screen.fill((0,0,0))
            
    def handle_draw(self, screen):
        score = u"Хамгийн өндөр оноонууд"
        text = self.font.render(score, True, (255,0,0))
        screen.blit(text,(self.pos[0],self.pos[1]-50))
        if self.edit and self.list[10][1]<self.player[1]:
            score = u"Нэрээ оруулаад enter товч дарна уу!"
            text = self.font.render(score, True, (255,0,0))
            screen.blit(text,(self.pos[0],self.pos[1]+10*35))
        count = 0
        for iter in self.list:
            s = u""
            s += iter[0]
            text = self.font.render(s, True, (255,255,255))                
            screen.blit(text, (self.pos[0],self.pos[1]+count*35))
            s = u""
            s += str(iter[1])
            text = self.font.render(s, True, (255,255,255))
            screen.blit(text, (self.pos[0]+300,self.pos[1]+count*35))
            if count>=9:
                break                
            count += 1
        pass
    
    def sortByScore(self,list):
        length = len(self.list)
        for i in range(0,length):
            for j in range(i+1,length):
                if self.list[i][1]<self.list[j][1]:
                    temp = self.list[i]
                    self.list[i] = self.list[j]
                    self.list[j] = temp
                    pass
                pass
            pass
        pass
    