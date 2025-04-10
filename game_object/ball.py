import pygame
import Box2D as b2 
import math
from  .game_object import GameObject, load_image_list, load_sound_asset 
from  settings     import PPM, MPP, TILE_SIZE, RED, SCREEN_HEIGHT


class Ball(GameObject):
    IMAGE_PATHS = [
        'data/image/ball/yellow_ball.png',
        'data/image/ball/red_ball.png',
        'data/image/ball/orange_ball.png',
        'data/image/ball/green_ball.png',
        'data/image/ball/black_ball.png',
        'data/image/ball/blue_ball.png'
    ]
    _loaded_images = None
    NUM_TYPES      = len(IMAGE_PATHS)

    _thump_sound = None
    _debug_font  = None 

    def __init__(self, game_state, world, start_pos_px, ball_type_index):
        super().__init__(world, b2.b2_dynamicBody)
        self.game_state = game_state 

        if Ball._loaded_images is None:
             Ball._loaded_images = load_image_list(Ball.IMAGE_PATHS)
        if Ball._thump_sound is None:
             Ball._thump_sound = load_sound_asset('data/sound/fx/thump.ogg')
             if Ball._thump_sound: Ball._thump_sound.set_volume(0.4) 
        if Ball._debug_font is None:
             Ball._debug_font = pygame.font.Font(None, 14) 

        self.ball_type   = ball_type_index % self.NUM_TYPES
        self.image       = Ball._loaded_images[self.ball_type] 
        self.thump_sound = Ball._thump_sound 
        self.debug_font  = Ball._debug_font

        if self.image:
            self.radius_px = self.image.get_width() / 2.0
            self.radius_m = self.radius_px * MPP
        else: 
             print(f"Error: Ball image {self.ball_type} not loaded. Using default radius.")
             self.radius_px = TILE_SIZE / 2.0 
             self.radius_m = self.radius_px * MPP

        self.create_body(start_pos_px) 
        if self.body: 
            shape = b2.b2CircleShape(radius=self.radius_m) 
            self.add_fixture(
                shape       = shape,
                density     = 0.8, 
                friction    = 0.3,
                restitution = 0.3 
            )
        else:
            print(f"Error: Failed to create physics body for Ball at {start_pos_px}")
            self.destroy()

        self.colliding_balls = set() 
        self.is_traversed    = False   
        self.chain_value     = 0        
        self.first_thump     = True     

    def begin_contact(self, other_object, contact):
        if isinstance(other_object, Ball) and other_object.ball_type == self.ball_type:
            if not other_object.marked_for_removal: 
                 self.colliding_balls.add(other_object)
        if self.first_thump and contact.enabled and contact.touching:
             if self.thump_sound:
                 self.thump_sound.play()
             self.first_thump = False 

    def end_contact(self, other_object, contact):
        if isinstance(other_object, Ball):
            self.colliding_balls.discard(other_object)

    # Chain Reaction Logic
    def _count_connected_chain_recursive(self, visited_set):
        if self in visited_set or self.marked_for_removal:
            return 0
        visited_set.add(self) 
        self.is_traversed = True 
        count = 1 
        for neighbor in list(self.colliding_balls):
            if neighbor and not neighbor.marked_for_removal:
                count += neighbor._count_connected_chain_recursive(visited_set)
        return count

    def _mark_chain_for_removal_recursive(self, marked_set):
         if self.marked_for_removal or self in marked_set:
             return
         marked_set.add(self) 
         self.destroy() 
         for neighbor in list(self.colliding_balls):
             if neighbor: 
                  neighbor._mark_chain_for_removal_recursive(marked_set)

    def check_and_remove_chain(self, min_chain_size=4):
        """
        Checking if this ball starts a chain of >= min_chain_size.
        If so, marks all balls in that chain for removal.
        Returns the number of balls marked for removal (0 if chain too small).
        Assumes self.is_traversed has been reset globally before calling this.
        """
        if self.marked_for_removal or self.is_traversed:
            return 0 

        # 1. Count the chain starting from this ball
        visited_in_count = set() 
        self.chain_value = self._count_connected_chain_recursive(visited_in_count)

        # 2. Mark for removal if chain is large enough
        if self.chain_value >= min_chain_size:
            marked_in_removal = set()
            self._mark_chain_for_removal_recursive(marked_in_removal)
            return self.chain_value 
        else:
            return 0

    def reset_traversal(self):
        self.is_traversed = False
        self.chain_value  = 0 

    def update(self, delta_time):
        if self.marked_for_removal: return 
        if self.body:
            pos_m = self.body.position
            if pos_m.y * PPM > SCREEN_HEIGHT + self.radius_px * 5: 
                self.destroy()
        else:
             if not self.marked_for_removal:
                  print(f"Warning: Ball {self} has no body during update. Marking for removal.")
                  self.destroy()

    def draw(self, screen):
        if self.marked_for_removal or not self.body or not self.image:
            return
        try:
            pos_px    = self.get_pixel_position() 
            angle_deg = self.get_angle_degrees() 
            rotated_image = pygame.transform.rotate(self.image, -angle_deg)
            rotated_rect = rotated_image.get_rect()
            rotated_rect.center = (int(pos_px[0]), int(pos_px[1]))
            screen.blit(rotated_image, rotated_rect.topleft)
        except Exception as e:
            print(f"Error drawing Ball {self}: {e}")
            pass

    def _draw_debug_connections(self, screen):
         if self.marked_for_removal or not self.body: return
         center_px = (int(self.body.position.x * PPM), int(self.body.position.y * PPM))
         for neighbor in self.colliding_balls:
             if neighbor and neighbor.body and not neighbor.marked_for_removal:
                 try:
                     neighbor_pos = (int(neighbor.body.position.x * PPM), int(neighbor.body.position.y * PPM))
                     pygame.draw.aaline(screen, (0,0,0,100), center_px, neighbor_pos) 
                 except: pass 

    def _draw_debug_info(self, screen):
         if self.marked_for_removal or not self.body or not self.debug_font: return
         center_px = (int(self.body.position.x * PPM), int(self.body.position.y * PPM))
         try:
             debug_text = f"T:{self.is_traversed}"
             text_surf = self.debug_font.render(debug_text, True, RED)
             text_rect = text_surf.get_rect(center=center_px)
             screen.blit(text_surf, text_rect)
         except: pass 