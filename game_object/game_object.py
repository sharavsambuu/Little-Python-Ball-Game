import pygame
import Box2D as b2 
import math
import os 
from   settings import PPM, MPP

_asset_cache = {}

def load_image_asset(path, use_cache=True):
    full_path = os.path.abspath(path) 
    if use_cache and full_path in _asset_cache:
        return _asset_cache[full_path]
    try:
        if not pygame.display.get_init():
             print(f"Warning: Trying to load image '{path}' before display is initialized.")
             image = pygame.image.load(full_path)
        else:
             image = pygame.image.load(full_path).convert_alpha()
        if use_cache:
             _asset_cache[full_path] = image
        return image
    except pygame.error as e:
        print(f"Error loading image '{path}': {e}")
        surf = pygame.Surface((int(PPM), int(PPM)), pygame.SRCALPHA) 
        surf.fill((255, 0, 255, 180)) 
        try: 
             pygame.draw.line(surf, (0, 0, 0), (0, 0), surf.get_size(), 1)
             pygame.draw.line(surf, (0, 0, 0), (0, surf.get_height()), (surf.get_width(), 0), 1)
        except: pass 
        if use_cache:
             _asset_cache[full_path] = surf
        return surf

def load_image_list(paths, use_cache=True):
    return [load_image_asset(p, use_cache) for p in paths]

def load_sound_asset(path, use_cache=True):
    full_path = os.path.abspath(path)
    if use_cache and full_path in _asset_cache:
        return _asset_cache[full_path]
    try:
        sound = pygame.mixer.Sound(full_path)
        if use_cache:
            _asset_cache[full_path] = sound
        return sound
    except pygame.error as e:
        print(f"Error loading sound '{path}': {e}")
        return None 


class GameObject:
    def __init__(self, world, body_type=b2.b2_dynamicBody, user_data=None): 
        self.world                    = world
        self.body                     = None
        valid_types                   = [b2.b2_staticBody, b2.b2_dynamicBody, b2.b2_kinematicBody]
        self.body_type                = body_type if body_type in valid_types else b2.b2_dynamicBody
        self.marked_for_removal       = False
        self.user_data                = user_data if user_data is not None else {}
        self.user_data['game_object'] = self 

    def create_body(self, position_px, angle_rad=0.0):
        if not self.world:
             return
        if self.body:
             print(f"Warning: Body already exists for this GameObject ({type(self).__name__}).")
             return 
        try:
            body_def          = b2.b2BodyDef() 
            body_def.type     = self.body_type
            body_def.position = b2.b2Vec2(position_px[0] * MPP, position_px[1] * MPP) 
            body_def.angle    = angle_rad
            body_def.userData = self.user_data 
            self.body         = self.world.CreateBody(body_def)
        except Exception as e:
            print(f"Error creating body for {type(self).__name__} at {position_px}: {e}")
            self.body = None 

    def add_fixture(self, shape, density=1.0, friction=0.3, restitution=0.1, is_sensor=False, fixture_user_data=None,
                    category_bits=0x0001, mask_bits=0xFFFF, group_index=0):
        if not self.body:
            return
        try:
            fixture_def                     = b2.b2FixtureDef(shape=shape) 
            fixture_def.density             = density 
            fixture_def.friction            = friction
            fixture_def.restitution         = restitution
            fixture_def.isSensor            = is_sensor
            fixture_def.userData            = fixture_user_data if fixture_user_data is not None else self.body.userData
            fixture_def.filter.categoryBits = category_bits
            fixture_def.filter.maskBits     = mask_bits
            fixture_def.filter.groupIndex   = group_index
            fixture = self.body.CreateFixture(fixture_def)
            return fixture 
        except Exception as e:
             print(f"Error adding fixture for {type(self).__name__}: {e}")
             return None

    def get_pixel_position(self):
        if not self.body:
             if hasattr(self, 'pos_px'): 
                 return self.pos_px
             return (0.0, 0.0)
        pos_m = self.body.position
        return (pos_m.x * PPM, pos_m.y * PPM)

    def get_angle_degrees(self):
        if not self.body:
             if hasattr(self, 'rotation_angle_deg'): 
                 return self.rotation_angle_deg
             return 0.0
        return math.degrees(self.body.angle)

    def begin_contact(self, other_object, contact):
        pass

    def end_contact(self, other_object, contact):
        pass

    def update(self, delta_time):
        if self.body and self.world and self.world.IsLocked():
             print(f"Warning: Accessing body properties for {type(self).__name__} while world is locked!")
             return 
    def draw(self, screen):
        raise NotImplementedError(f"Draw method not implemented for {type(self).__name__}")

    def destroy(self):
        if not self.marked_for_removal:
            self.marked_for_removal = True

    def _draw_debug_fixture(self, screen, fixture, transform, color):
         shape = fixture.shape
         try:
             if isinstance(shape, b2.b2PolygonShape): 
                 vertices = [(transform * v) * PPM for v in shape.vertices]
                 vertices = [(int(v.x), int(v.y)) for v in vertices]
                 if len(vertices) > 1:
                     if len(vertices) == 2: pygame.draw.aaline(screen, color, vertices[0], vertices[1])
                     else: pygame.draw.polygon(screen, color, vertices, 1) 
             elif isinstance(shape, b2.b2CircleShape): 
                 center_m  = transform * shape.pos 
                 center_px = (int(center_m.x * PPM), int(center_m.y * PPM))
                 radius_px = int(shape.radius * PPM)
                 if radius_px > 0:
                     pygame.draw.circle(screen, color, center_px, radius_px, 1)
                     body_angle = transform.angle 
                     end_point_px = (center_px[0] + radius_px * math.cos(body_angle),
                                     center_px[1] + radius_px * math.sin(body_angle))
                     pygame.draw.line(screen, color, center_px, (int(end_point_px[0]), int(end_point_px[1])), 1)
         except Exception as e:
             pass

    def draw_debug(self, screen, color=(255, 0, 0)):
         if not self.body:
             return 
         transform = self.body.transform
         for fixture in self.body.fixtures:
              fixture_color = color
              if fixture.isSensor:
                   fixture_color = (color[0]//2, color[1]//2, 255) 
              self._draw_debug_fixture(screen, fixture, transform, fixture_color)