import pygame
import Box2D as b2 
from  .game_object import GameObject, load_image_asset 
from  settings     import PPM, MPP, TILE_SIZE


class StaticBox(GameObject):
    IMAGE_PATH = 'data/image/box/box.png'
    _image     = None

    def __init__(self, world, center_pos_px):
        super().__init__(world, b2.b2_staticBody)
        if StaticBox._image is None:
             StaticBox._image = load_image_asset(StaticBox.IMAGE_PATH)
        self.image = StaticBox._image

        if not self.image:
            print("Error: StaticBox image failed to load. Using default size.")
            self.half_width_px  = TILE_SIZE / 2.0
            self.half_height_px = TILE_SIZE / 2.0
        else:
            self.half_width_px  = self.image.get_width() / 2.0
            self.half_height_px = self.image.get_height() / 2.0

        self.half_width_m = self.half_width_px * MPP
        self.half_height_m = self.half_height_px * MPP

        self.create_body(center_pos_px) 
        if self.body:
            shape = b2.b2PolygonShape(box=(self.half_width_m, self.half_height_m)) 
            self.add_fixture(
                shape       = shape,
                friction    = 0.95, 
                restitution = 0.1 
                )
        else:
            print(f"Error: Failed to create physics body for StaticBox at {center_pos_px}")
            self.destroy() 

    def draw(self, screen):
        if self.marked_for_removal or not self.body or not self.image:
            return 
        try:
            pos_px    = self.get_pixel_position() 
            angle_deg = self.get_angle_degrees()

            if angle_deg == 0:
                rect = self.image.get_rect(center=(int(pos_px[0]), int(pos_px[1])))
                screen.blit(self.image, rect.topleft)
            else:
                rotated_image = pygame.transform.rotate(self.image, -angle_deg)
                rect          = rotated_image.get_rect(center=(int(pos_px[0]), int(pos_px[1])))
                screen.blit(rotated_image, rect.topleft)

        except Exception as e:
             print(f"Error drawing StaticBox: {e}")