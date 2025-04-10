import pygame
import Box2D as b2 
import math
from state import State
from settings import (
    PPM, MPP, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, YELLOW,
    K_RETURN, K_PAUSE_QUIT, FONT_PATH,
    DEATH_STATE_GRAVITY 
)

class Death(State):
    VELOCITY_ITERATIONS = 8
    POSITION_ITERATIONS = 3
    TIME_STEP           = 1.0 / 60.0
    _font               = None

    def __init__(self):
        super().__init__()
        self.world               = None
        self.message_body        = None
        self.message_surface     = None
        self.font                = None
        self.time_passed         = 0.0
        self.delay               = 3.5 
        self.next_state_key      = 'score'
        self.next_state_params   = {}
        self.background_snapshot = None
        self.shader_surface      = None
        self.physics_accumulator = 0.0
        self._load_assets()

    def _load_assets(self):
        if Death._font is None:
            try:
                Death._font = pygame.font.Font(FONT_PATH, 70)
            except pygame.error as e:
                print(f"Error loading font '{FONT_PATH}' for Death state: {e}")
                Death._font = pygame.font.Font(None, 80) 
        self.font = Death._font

    def _setup_world(self):
        if self.world:
            print("Warning: World already exists in Death state setup.")
            return
        try:
            self.world = b2.b2World(gravity=DEATH_STATE_GRAVITY, doSleep=True)
            print(f"Death state world created with gravity: {DEATH_STATE_GRAVITY}")
            self._create_floor() 
        except Exception as e:
            print(f"Error creating Box2D world in Death state: {e}")
            self.world = None

    def _create_floor(self):
        if not self.world: print("Cannot create floor: World not initialized."); return
        try:
            floor_body_def          = b2.b2BodyDef()
            floor_pos_px            = (SCREEN_WIDTH / 2.0, SCREEN_HEIGHT + TILE_SIZE ) 
            floor_body_def.position = (floor_pos_px[0] * MPP, floor_pos_px[1] * MPP)
            floor_body_def.type     = b2.b2_staticBody
            floor_body              = self.world.CreateBody(floor_body_def)
            floor_half_width_m      = (SCREEN_WIDTH / 2.0) * MPP
            floor_half_height_m     = TILE_SIZE * MPP # Make it thicker
            shape                   = b2.b2PolygonShape(box=(floor_half_width_m, floor_half_height_m))
            floor_body.CreateFixture(shape=shape, friction=0.8, restitution=0.1) # Low bounce
        except Exception as e: print(f"Error creating floor in Death state: {e}")

    def _create_message_body(self):
        if not self.font or not self.world: print("Cannot create message body: Font or world not ready."); return
        self._destroy_message_body() 
        try:
            text                 = "Game Over"
            self.message_surface = self.font.render(text, True, WHITE)
            msg_width_px         = self.message_surface.get_width()
            msg_height_px        = self.message_surface.get_height()

            body_def          = b2.b2BodyDef()
            body_def.type     = b2.b2_dynamicBody
            start_pos_px      = (SCREEN_WIDTH * 0.5, -msg_height_px * 1.5) 
            body_def.position = (start_pos_px[0] * MPP, start_pos_px[1] * MPP)
            body_def.angle    = math.radians(randint(-10, 10)) 
            body_def.userData = {"type": "death_message"}

            self.message_body = self.world.CreateBody(body_def)

            shape = b2.b2PolygonShape(box=(msg_width_px / 2.0 * MPP, msg_height_px / 2.0 * MPP))
            fixture_def = b2.b2FixtureDef(
                shape=shape,
                density=1.5, friction=0.6, restitution=0.4 
            )
            self.message_body.CreateFixture(fixture_def)
            self.message_body.ApplyAngularImpulse(uniform(-0.5, 0.5) * self.message_body.inertia, True)
            print("Death message body created.")
        except Exception as e:
            print(f"Error creating message body: {e}")
            self.message_body = None

    def _destroy_message_body(self):
        if self.message_body and self.world:
            try: self.world.DestroyBody(self.message_body)
            except Exception as e: print(f"Error destroying message body: {e}")
        self.message_body    = None
        self.message_surface = None

    def handle_enter(self, parameters):
        print("Entering Death State")
        self.next_state_key      = parameters.get('next_state', 'score')
        score_params             = { 'total_score': parameters.get('total_score', 0), 'edit': True }
        self.next_state_params   = score_params
        self.delay               = parameters.get('delay', 3.5)
        self.time_passed         = 0.0
        self.physics_accumulator = 0.0
        self.background_snapshot = None
        self.shader_surface      = None
        self._setup_world() 
        self._create_message_body()

    def handle_exit(self):
        print("Exiting Death State")
        self._destroy_message_body()
        self.world               = None
        self.background_snapshot = None

    def handle_keydown(self, key):
        if key in (K_RETURN, K_PAUSE_QUIT) and self.engine:
             print("Skipping death animation...")
             self.engine.change_state(self.next_state_key, self.next_state_params)

    def handle_update(self, delta_time):
        if self.world:
            self.physics_accumulator += delta_time
            while self.physics_accumulator >= self.TIME_STEP:
                try:
                    self.world.Step(self.TIME_STEP, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
                    self.world.ClearForces()
                except Exception as e:
                     print(f"Error during world step in Death state: {e}")
                     break
                self.physics_accumulator -= self.TIME_STEP
        self.time_passed += delta_time
        if self.time_passed >= self.delay:
            if self.engine:
                self.engine.change_state(self.next_state_key, self.next_state_params)

    def handle_erase(self, screen):
        if self.background_snapshot is None and self.engine and hasattr(self.engine, 'screen'):
            try: self.background_snapshot = self.engine.screen.copy()
            except pygame.error as e:
                 print(f"Error copying screen for background: {e}")
                 self.background_snapshot = pygame.Surface(SCREEN_SIZE); self.background_snapshot.fill(BLACK)
        if self.background_snapshot: screen.blit(self.background_snapshot, (0, 0))
        else: screen.fill(BLACK)

    def handle_draw(self, screen):
        if self.shader_surface is None:
            try: self.shader_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            except pygame.error as e: print(f"Error creating shader surface: {e}")
        if self.shader_surface:
            alpha = min(180, int(255 * (self.time_passed / self.delay)))
            self.shader_surface.fill((0, 0, 0, alpha))
            screen.blit(self.shader_surface, (0, 0))
        if self.message_body and self.message_surface:
            try:
                pos_m = self.message_body.position
                pos_px = (pos_m.x * PPM, pos_m.y * PPM)
                angle_deg = math.degrees(self.message_body.angle)
                rotated_msg = pygame.transform.rotate(self.message_surface, -angle_deg)
                rotated_rect = rotated_msg.get_rect(center=(int(pos_px[0]), int(pos_px[1])))
                screen.blit(rotated_msg, rotated_rect.topleft)
            except Exception as e: pass 
        # self._draw_debug(screen) 
