import pygame
import Box2D as b2 
import math
from  .game_object import GameObject, load_image_asset 
from  settings     import PPM, MPP, TILE_SIZE 


class DynamicBox(GameObject):
    IMAGE_PATH = 'data/image/box/sharavaa.jpg' 
    _image     = None
    def __init__(self, world, center_pos_px, angle_deg=0):
        super().__init__(world, b2.b2_dynamicBody)
        if DynamicBox._image is None:
             DynamicBox._image = load_image_asset(DynamicBox.IMAGE_PATH)
        self.image = DynamicBox._image

        if not self.image:
            print(f"Error: DynamicBox image '{self.IMAGE_PATH}' failed to load. Using default size.")
            self.half_width_px  = TILE_SIZE / 2.0 
            self.half_height_px = TILE_SIZE / 2.0
        else:
            self.half_width_px  = self.image.get_width()  / 2.0
            self.half_height_px = self.image.get_height() / 2.0

        self.half_width_m  = self.half_width_px  * MPP
        self.half_height_m = self.half_height_px * MPP

        angle_rad = math.radians(angle_deg)

        self.create_body(center_pos_px, angle_rad=angle_rad) 
        if self.body:
            shape = b2.b2PolygonShape(box=(self.half_width_m, self.half_height_m)) 
            self.add_fixture(
                shape       = shape,
                density     = 1.0, 
                friction    = 0.5,
                restitution = 0.2
            )
        else:
            print(f"Error: Failed to create physics body for DynamicBox at {center_pos_px}")
            self.destroy()

    def draw(self, screen):
        if self.marked_for_removal or not self.body or not self.image:
            return 
        try:
            pos_px    = self.get_pixel_position() 
            angle_deg = self.get_angle_degrees() 
            rotated_image = pygame.transform.rotate(self.image, -angle_deg)
            rect          = rotated_image.get_rect(center=(int(pos_px[0]), int(pos_px[1])))
            screen.blit(rotated_image, rect.topleft)
        except Exception as e:
             print(f"Error drawing DynamicBox: {e}")