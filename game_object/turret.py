import pygame
import math
import Box2D as b2
from   random       import randint, uniform
from   .game_object import GameObject, load_image_asset, load_image_list
from   .ball        import Ball
from   settings     import PPM, MPP, TILE_SIZE


class Turret(GameObject):
    TURRET_IMAGE_PATH = 'data/image/turrent/turrent.png'
    BALL_IMAGE_PATHS  = Ball.IMAGE_PATHS
    NUM_BALL_TYPES    = Ball.NUM_TYPES
    _turret_image     = None
    _ball_images      = None

    def __init__(self, game_state, position_px):
        super().__init__(world=None, body_type=None)
        self.game_state = game_state
        self.pos_px     = list(map(float, position_px))

        if Turret._turret_image is None: Turret._turret_image = load_image_asset(Turret.TURRET_IMAGE_PATH)
        if Turret._ball_images is None:
             if Ball._loaded_images: Turret._ball_images = Ball._loaded_images
             else: Turret._ball_images = load_image_list(Turret.BALL_IMAGE_PATHS)

        self.image               = Turret._turret_image
        self.preview_ball_images = Turret._ball_images
        self.valid               = bool(self.image and self.preview_ball_images and any(self.preview_ball_images))
        if not self.valid: print("Error: Turret or preview ball images failed to load.")

        self.rotation_angle_deg = 0.0 
        self.shoot_requested    = False
        self.shoot_cooldown     = 0.2
        self.shoot_timer        = self.shoot_cooldown

        if self.NUM_BALL_TYPES > 0: self.next_ball_type = randint(0, self.NUM_BALL_TYPES - 1)
        else: print("Error: NUM_BALL_TYPES is zero."); self.next_ball_type = 0; self.valid = False

    def update(self, delta_time):
        if not self.valid: return
        mouse_pos                = pygame.mouse.get_pos()
        dx                       = mouse_pos[0] - self.pos_px[0]
        dy                       = -(mouse_pos[1] - self.pos_px[1])
        target_angle_rad         = math.atan2(dy, dx)
        target_angle_deg         = math.degrees(target_angle_rad)
        min_angle_atan2          = 10
        max_angle_atan2          = 170
        clamped_target_angle_deg = max(min_angle_atan2, min(target_angle_deg, max_angle_atan2))
        self.rotation_angle_deg  = clamped_target_angle_deg - 90

        if self.shoot_timer < self.shoot_cooldown: self.shoot_timer += delta_time

        if self.shoot_requested and self.shoot_timer >= self.shoot_cooldown:
            self._shoot()
            self.shoot_timer     = 0.0
            self.shoot_requested = False
        else:
             self.shoot_requested = False

    def request_shoot(self):
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_requested = True

    def _get_shoot_direction(self):
        shoot_angle_rad = math.radians(self.rotation_angle_deg + 90)
        dir_x           = math.cos(shoot_angle_rad)
        math_dir_y      = math.sin(shoot_angle_rad)
        physics_dir_y   = -math_dir_y
        direction       = b2.b2Vec2(dir_x, physics_dir_y)
        if direction.length < 1e-6: return None
        direction.Normalize()
        return direction

    def _shoot(self):
        if not self.valid: return
        if not self.game_state or not self.game_state.world: print("Error: Shoot - No game_state/world"); return
        if self.NUM_BALL_TYPES <= 0: print("Error: Shoot - No ball types"); return

        direction = self._get_shoot_direction()
        if not direction: print("Warning: Shoot direction is zero/invalid."); return

        ball_radius_px = TILE_SIZE / 2.0
        if self.preview_ball_images and 0 <= self.next_ball_type < len(self.preview_ball_images):
             preview_img = self.preview_ball_images[self.next_ball_type]
             if preview_img: ball_radius_px = preview_img.get_width() / 2.0
        spawn_offset_px = (TILE_SIZE * 0.4) + ball_radius_px + 2

        spawn_pos_px = (self.pos_px[0] + direction.x * spawn_offset_px,
                        self.pos_px[1] + direction.y * spawn_offset_px) 

        bullet = Ball(self.game_state, self.game_state.world, spawn_pos_px, self.next_ball_type)

        if bullet.body:
            shoot_speed = 25.0
            impulse     = bullet.body.mass * direction * shoot_speed
            bullet.body.ApplyLinearImpulse(impulse, bullet.body.worldCenter, True)
            self.game_state.add_game_object(bullet)
            self.next_ball_type = randint(0, self.NUM_BALL_TYPES - 1)
        else:
            print("Error: Failed to create bullet body.")

    def draw(self, screen):
        if not self.valid: return
        try:
            if self.preview_ball_images and 0 <= self.next_ball_type < len(self.preview_ball_images):
                next_ball_image = self.preview_ball_images[self.next_ball_type]
                if next_ball_image:
                    next_ball_rect = next_ball_image.get_rect(center=(int(self.pos_px[0]), int(self.pos_px[1])))
                    screen.blit(next_ball_image, next_ball_rect.topleft)
            if self.image:
                rotated_turret = pygame.transform.rotate(self.image, self.rotation_angle_deg)
                turret_rect = rotated_turret.get_rect(center=(int(self.pos_px[0]), int(self.pos_px[1])))
                screen.blit(rotated_turret, turret_rect.topleft)
        except Exception as e: print(f"Error drawing Turret: {e}")