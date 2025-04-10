import pygame
from random       import randint, uniform
from .game_object import GameObject, load_image_asset 
from settings     import SCREEN_WIDTH, SCREEN_HEIGHT


class Cloud(GameObject):
    IMAGE_PATH = 'data/image/cloud/cloud.png'
    _image     = None
    def __init__(self, start_pos_px=None):
        super().__init__(world=None, body_type=None)

        if Cloud._image is None:
             Cloud._image = load_image_asset(Cloud.IMAGE_PATH)
        self.image = Cloud._image

        if not self.image: 
            print("Error: Cloud image failed to load.")
            self.valid = False
            return
        else:
            self.valid = True

        self.pos_px = [0.0, 0.0]
        if start_pos_px:
            self.pos_px = list(map(float, start_pos_px))
            self.speed = uniform(15, 40) 
        else:
            self.reset(assign_random_speed=True) 

    def reset(self, assign_random_speed=True):
         if not self.valid: return 
         self.pos_px[0] = float(SCREEN_WIDTH + randint(50, self.image.get_width() * 2))
         self.pos_px[1] = float(uniform(0, SCREEN_HEIGHT * 0.6 - self.image.get_height()))
         if assign_random_speed:
             self.speed = uniform(15, 40) 

    def update(self, delta_time):
        if not self.valid: return 
        self.pos_px[0] -= self.speed * delta_time
        if self.pos_px[0] + self.image.get_width() < 0:
            self.reset() 

    def draw(self, screen):
        if not self.valid or not self.image: return 
        try:
            screen.blit(self.image, (int(self.pos_px[0]), int(self.pos_px[1])))
        except Exception as e:
             print(f"Error drawing Cloud: {e}")