import pygame
import Box2D as b2 
import math
from random import randint

from state import State
from settings import (
    PPM, MPP, TILE_SIZE, TILE_DIM, BLUE, WHITE, YELLOW,
    K_PAUSE_QUIT, FONT_PATH, SCREEN_WIDTH, SCREEN_HEIGHT,
    GAME_GRAVITY 
)
from game_object import ( 
    GameObject, Ball, StaticBox, Turret, Cloud, BallAdder, PercentDisplay, ComboTracker,
    load_sound_asset 
)
from settings import SOUND_FX_POP, SOUND_MUSIC_GAME


class GameContactListener(b2.b2ContactListener):
    def __init__(self, game_state):
        b2.b2ContactListener.__init__(self)
        self.game_state = game_state 
    def _get_object_from_contact(self, contact_fixture):
        if contact_fixture and contact_fixture.body and contact_fixture.body.userData:
            user_data = contact_fixture.body.userData
            if isinstance(user_data, dict) and 'game_object' in user_data:
                 return user_data['game_object']
            elif isinstance(user_data, GameObject): 
                 return user_data
        return None
    def BeginContact(self, contact):
        obj_a = self._get_object_from_contact(contact.fixtureA)
        obj_b = self._get_object_from_contact(contact.fixtureB)
        if obj_a: obj_a.begin_contact(obj_b, contact)
        if obj_b: obj_b.begin_contact(obj_a, contact)
    def EndContact(self, contact):
        obj_a = self._get_object_from_contact(contact.fixtureA)
        obj_b = self._get_object_from_contact(contact.fixtureB)
        if obj_a: obj_a.end_contact(obj_b, contact)
        if obj_b: obj_b.end_contact(obj_a, contact)

class Game(State):
    VELOCITY_ITERATIONS = 8
    POSITION_ITERATIONS = 3
    PHYSICS_TIME_STEP   = 1.0 / 60.0
    INITIAL_BALLS       = 30 
    MAX_BALL_CAPACITY   = 200
    _ui_font      = None
    _percent_font = None
    _pop_sound    = None
    def __init__(self):
        super().__init__()
        self.world               = None
        self.contact_listener    = None
        self.game_objects        = []
        self.turret              = None
        self.ball_adder          = None
        self.percent_display     = None
        self.combo_tracker       = None
        self.clouds              = []
        self.score               = 0
        self.current_ball_count  = 0
        self.ball_fill_percent   = 0
        self.paused              = False
        self.physics_accumulator = 0.0
        self.ui_font             = None
        self.percent_font        = None
        self.pop_sound           = None
        self.music_path          = SOUND_MUSIC_GAME
        self._load_assets()
    def _load_assets(self):
        if Game._ui_font is None:
            try:
                Game._ui_font      = pygame.font.Font(FONT_PATH, 28)
                Game._percent_font = pygame.font.Font(FONT_PATH, 24)
            except pygame.error as e:
                print(f"Error loading font '{FONT_PATH}' for Game state: {e}")
                Game._ui_font = pygame.font.Font(None, 30) 
                Game._percent_font = pygame.font.Font(None, 26)
        self.ui_font      = Game._ui_font
        self.percent_font = Game._percent_font
        if Game._pop_sound is None:
             Game._pop_sound = load_sound_asset(SOUND_FX_POP)
             if Game._pop_sound: Game._pop_sound.set_volume(0.5)
        self.pop_sound = Game._pop_sound
    def _setup_world(self):
         print("Setting up Box2D world...")
         if self.world:
             print("Warning: World already exists during setup. Recreating.")
         try:
             self.world = b2.b2World(gravity=GAME_GRAVITY, doSleep=True)
             print(f"World created with gravity: {GAME_GRAVITY}")
             self.contact_listener = GameContactListener(self)
             self.world.contactListener = self.contact_listener
             print("Box2D World listener set.")
         except Exception as e:
             print(f"FATAL: Failed to create Box2D world: {e}")
             self.world = None
             if self.engine: self.engine.exit()
    def _clear_objects(self):
         print("Clearing game objects...")
         if self.world:
             body_count      = self.world.bodyCount
             destroyed_count = 0
             body            = self.world.GetBodyList()
             while body:
                 next_body = body.GetNext()
                 game_obj  = self._get_object_from_body(body)
                 if game_obj:
                     game_obj.body = None
                 try:
                     self.world.DestroyBody(body)
                     destroyed_count += 1
                 except Exception as e: print(f"Error destroying body: {e}")
                 body = next_body
             print(f"Destroyed {destroyed_count}/{body_count} bodies.")
         else: print("Warning: World not available during object clearing.")
         self.game_objects    = []
         self.clouds          = []
         self.turret          = None
         self.ball_adder      = None
         self.percent_display = None
         self.combo_tracker   = None
         print("Game object lists cleared.")
    def _get_object_from_body(self, body):
        if body and body.userData:
            user_data = body.userData
            if isinstance(user_data, dict) and 'game_object' in user_data:
                 return user_data['game_object']
            elif isinstance(user_data, GameObject): return user_data
        return None
    def _create_boundaries(self):
        if not self.world:
            print("Error: Cannot create boundaries, world not setup.")
            return
        print("Creating boundaries (Top, Left, Right)...")

        wall_friction    = 0.3 
        wall_restitution = 0.1 
        half_tile_m      = (TILE_SIZE / 2.0) * MPP
        boundary_defs    = [] 

        center_x_px   = (TILE_DIM[0] * TILE_SIZE) / 2.0
        center_y_px   = -half_tile_m / MPP 
        half_width_m  = (TILE_DIM[0] * TILE_SIZE / 2.0) * MPP
        half_height_m = half_tile_m
        boundary_defs.append(((center_x_px, center_y_px), (half_width_m, half_height_m), {"type": "boundary_top"}))

        center_x_px   = -half_tile_m / MPP 
        center_y_px   = (TILE_DIM[1] * TILE_SIZE) / 2.0
        half_width_m  = half_tile_m
        half_height_m = (TILE_DIM[1] * TILE_SIZE / 2.0) * MPP 
        boundary_defs.append(((center_x_px, center_y_px), (half_width_m, half_height_m), {"type": "boundary_left"}))

        center_x_px   = (TILE_DIM[0] * TILE_SIZE) + half_tile_m / MPP 
        center_y_px   = (TILE_DIM[1] * TILE_SIZE) / 2.0
        half_width_m  = half_tile_m
        half_height_m = (TILE_DIM[1] * TILE_SIZE / 2.0) * MPP 
        boundary_defs.append(((center_x_px, center_y_px), (half_width_m, half_height_m), {"type": "boundary_right"}))

        for pos_px, half_dims_m, user_data in boundary_defs:
            try:
                body_def = b2.b2BodyDef(
                    position=(pos_px[0] * MPP, pos_px[1] * MPP),
                    type=b2.b2_staticBody
                )
                body = self.world.CreateBody(body_def)
                shape = b2.b2PolygonShape(box=half_dims_m)
                body.userData = user_data 
                body.CreateFixture(shape=shape, friction=wall_friction, restitution=wall_restitution)
            except Exception as e:
                 print(f"Error creating boundary ({user_data['type']}) at {pos_px}: {e}")
        print("Boundaries created.")

    def _create_initial_objects(self):
         if not self.world:
             print("Error: Cannot create initial objects, world not setup.")
             return
         print("Creating initial objects...")

         turret_x    = TILE_DIM[0] * TILE_SIZE / 2.0
         turret_y    = (TILE_DIM[1] * TILE_SIZE) - (TILE_SIZE * 1.5) 
         self.turret = Turret(self, (turret_x, turret_y))

         self.ball_adder = BallAdder(self)
         self.add_game_object(self.ball_adder)

         display_x      = (TILE_DIM[0] + 0.5) * TILE_SIZE
         display_y      = TILE_SIZE * 2
         display_width  = TILE_SIZE * 3
         display_height = TILE_SIZE * 10
         self.percent_display = PercentDisplay((display_x, display_y), (display_width, display_height))

         self.combo_tracker = ComboTracker(self)
         self.add_game_object(self.combo_tracker)

         min_x = TILE_SIZE * 2 
         max_x = (TILE_DIM[0] - 2) * TILE_SIZE
         min_y = (TILE_DIM[1] / 2) * TILE_SIZE
         max_y = (TILE_DIM[1] - 4) * TILE_SIZE 

         print(f"Adding {self.INITIAL_BALLS} initial balls (spawning lower)...")
         added_count = 0
         for i in range(self.INITIAL_BALLS):
              pos_x = randint(int(min_x), int(max_x))
              pos_y = randint(int(min_y), int(max_y)) 
              ball_type = randint(0, Ball.NUM_TYPES - 1)
              ball = Ball(self, self.world, (pos_x, pos_y), ball_type)
              if ball.body:
                  self.add_game_object(ball)
                  added_count += 1
              else:
                  print(f"Warning: Failed to create body for initial ball {i+1}")
         print(f"{added_count}/{self.INITIAL_BALLS} initial balls added.")

         self.clouds = [Cloud() for _ in range(8)]
         print("Initial clouds created.")
         print("Initial objects creation complete.")

    def add_game_object(self, obj):
         if isinstance(obj, GameObject):
             if obj not in self.game_objects: self.game_objects.append(obj)
         else: print(f"Warning: Tried to add non-GameObject: {obj}")

    def add_score(self, points):
         if points > 0: self.score += points

    def reset_game(self):
        print("Resetting game...")
        self.paused = True
        self._clear_objects()
        self._setup_world() 
        self.score               = 0
        self.current_ball_count  = 0
        self.ball_fill_percent   = 0
        self.physics_accumulator = 0.0
        self._create_boundaries() 
        self._create_initial_objects() 
        self.paused = False
        print("Game reset complete.")

    def handle_enter(self, parameters):
        print("Entering Game State")
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        is_new_game = parameters.get('new', True)
        music_on = parameters.get("Music", True)
        if is_new_game or not self.world:
            print(f"Starting {'New' if is_new_game else 'Forced New'} Game...")
            self.reset_game()
        else:
            print("Resuming Game...")
            self.paused = False
        if music_on:
             if not pygame.mixer.music.get_busy():
                 try:
                     pygame.mixer.music.load(self.music_path)
                     pygame.mixer.music.set_volume(0.6)
                     pygame.mixer.music.play(-1)
                     print(f"Music started: {self.music_path}")
                 except pygame.error as e: print(f"Error loading/playing game music '{self.music_path}': {e}")
             else: print("Music already playing.")
        else:
            pygame.mixer.music.stop()
            print("Music stopped (setting is off).")

    def handle_exit(self):
        print("Exiting Game State")
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        self.paused = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN: self.handle_keydown(event.key)
        elif event.type == pygame.KEYUP: self.handle_keyup(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN: self.handle_mouse_button_down(event.button, event.pos)

    def handle_keydown(self, key):
        if key == K_PAUSE_QUIT:
            print("Pause/Quit key pressed.")
            self.paused = True
            menu_params = {}
            if self.engine: self.engine.change_state('menu', menu_params)
        elif key == pygame.K_F1: 
            self._draw_debug_flag = not getattr(self, '_draw_debug_flag', False)
            print(f"Debug Draw {'Enabled' if self._draw_debug_flag else 'Disabled'}")
        elif key == pygame.K_g: 
             if self.world:
                  current_g = self.world.gravity
                  new_g = b2.b2Vec2(current_g.x, -current_g.y) 
                  self.world.gravity = new_g
                  print(f"Gravity manually toggled to: {self.world.gravity}")

    def handle_keyup(self, key): pass

    def handle_mouse_button_down(self, button, position):
        if button == 1 and self.turret and not self.paused:
            self.turret.request_shoot()

    def handle_update(self, delta_time):
        if self.paused or not self.world: return

        self.physics_accumulator += delta_time
        steps_taken               = 0
        max_steps                 = 5
        while self.physics_accumulator >= self.PHYSICS_TIME_STEP and steps_taken < max_steps:
            try:
                self.world.Step(self.PHYSICS_TIME_STEP, self.VELOCITY_ITERATIONS, self.POSITION_ITERATIONS)
                self.world.ClearForces()
            except Exception as e:
                 print(f"Error during world step: {e}")
                 self.physics_accumulator = 0
                 break
            self.physics_accumulator -= self.PHYSICS_TIME_STEP
            steps_taken += 1

        current_game_objects = list(self.game_objects)
        for obj in current_game_objects:
             if not obj.marked_for_removal: obj.update(delta_time)

        if self.turret: self.turret.update(delta_time)
        if self.percent_display: self.percent_display.update(delta_time)
        for cloud in self.clouds: cloud.update(delta_time)

        # Chain Reaction
        balls_to_check = [obj for obj in self.game_objects if isinstance(obj, Ball) and not obj.marked_for_removal]
        for ball in balls_to_check: ball.reset_traversal()
        chains_found_this_frame = False
        total_removed_in_chains = 0
        for ball in balls_to_check:
             if not ball.is_traversed:
                 removed_count = ball.check_and_remove_chain(min_chain_size=4)
                 if removed_count > 0:
                     self.add_score(max(0, removed_count - 3))
                     total_removed_in_chains += removed_count
                     chains_found_this_frame = True
        if chains_found_this_frame:
            if self.pop_sound: self.pop_sound.play()
            if self.combo_tracker: self.combo_tracker.record_pop()

        bodies_to_destroy                = []
        remaining_objects                = []
        current_ball_count_after_removal = 0
        for obj in self.game_objects:
            if obj.marked_for_removal:
                if obj.body:
                    bodies_to_destroy.append(obj.body)
                    obj.body = None
            else:
                remaining_objects.append(obj)
                if isinstance(obj, Ball): current_ball_count_after_removal += 1
        if bodies_to_destroy:
             for body in bodies_to_destroy:
                 try: self.world.DestroyBody(body)
                 except Exception as e: pass 
        self.game_objects = remaining_objects
        self.current_ball_count = current_ball_count_after_removal

        if self.MAX_BALL_CAPACITY > 0:
            self.ball_fill_percent = int((self.current_ball_count * 100) / self.MAX_BALL_CAPACITY)
            self.ball_fill_percent = max(0, min(100, self.ball_fill_percent))
        else: self.ball_fill_percent = 0
        if self.percent_display: self.percent_display.update_percent(self.ball_fill_percent)

        if self.current_ball_count >= self.MAX_BALL_CAPACITY:
             print(f"Game Over - Ball capacity reached! ({self.current_ball_count}/{self.MAX_BALL_CAPACITY})")
             if self.engine and 'menu' in self.engine.states: 
                  menu_state = self.engine.states['menu']
                  if hasattr(menu_state, 'menu_structure'):
                      try:
                          for item_data in menu_state.menu_structure:
                               if isinstance(item_data, list) and len(item_data) > 1:
                                    if item_data[0] == "Resume" and item_data[1] == "game":
                                         if len(item_data) > 2 and isinstance(item_data[2], dict): item_data[2]['new'] = True
                                         elif len(item_data) == 2: item_data.append({'new': True})
                                         print("Menu 'Resume' option set to force new game.")
                                         break
                      except Exception as e: print(f"Error modifying menu state: {e}")
             if self.engine: 
                 death_params = {'total_score': self.score, 'edit': True, 'next_state': 'score'}
                 self.engine.change_state('death', death_params)
             self.paused = True

    def handle_erase(self, screen):
        screen.fill(BLUE)

    def handle_draw(self, screen):
        for cloud in self.clouds: cloud.draw(screen)
        for obj in self.game_objects:
             try: obj.draw(screen)
             except Exception as e: print(f"Error drawing object {type(obj)}: {e}")
        if self.turret: self.turret.draw(screen)
        if self.percent_display: self.percent_display.draw(screen)
        ui_area_x = (TILE_DIM[0] + 0.5) * TILE_SIZE
        score_pos = (ui_area_x, TILE_SIZE * 0.5)
        percent_label_y = (self.percent_display.outer_rect.bottom + 10 if self.percent_display else SCREEN_HEIGHT - TILE_SIZE * 2)
        if self.ui_font:
            try:
                score_surf = self.ui_font.render(f"Score: {self.score}", True, WHITE)
                screen.blit(score_surf, score_surf.get_rect(topleft=score_pos))
            except Exception as e: print(f"Error rendering score text: {e}")
        if self.percent_font and self.percent_display:
            try:
                 percent_surf = self.percent_font.render(f"{self.ball_fill_percent}% Full", True, WHITE)
                 screen.blit(percent_surf, percent_surf.get_rect(centerx=self.percent_display.outer_rect.centerx, top=percent_label_y))
            except Exception as e: print(f"Error rendering percent text: {e}")
        if getattr(self, '_draw_debug_flag', False): self._draw_debug_physics(screen)


    def _draw_debug_physics(self, screen):
         if not self.world: return
         for body in self.world.bodies:
             transform = body.transform
             color = (0, 255, 0) if body.type == b2.b2_staticBody else (255, 0, 0) if body.type == b2.b2_dynamicBody else (0, 0, 255)
             for fixture in body.fixtures:
                  try:
                      shape = fixture.shape
                      if isinstance(shape, b2.b2PolygonShape):
                          vertices = [(transform * v) * PPM for v in shape.vertices]
                          vertices = [(int(v.x), int(v.y)) for v in vertices]
                          if len(vertices) > 1: pygame.draw.polygon(screen, color, vertices, 1)
                      elif isinstance(shape, b2.b2CircleShape):
                          center_m = transform * shape.pos
                          center_px = (int(center_m.x * PPM), int(center_m.y * PPM))
                          radius_px = int(shape.radius * PPM)
                          if radius_px > 0:
                              pygame.draw.circle(screen, color, center_px, radius_px, 1)
                              angle_vec = transform.R.GetXAxis()
                              end_point_px = (center_px[0] + radius_px * angle_vec.x, center_px[1] + radius_px * angle_vec.y)
                              pygame.draw.line(screen, color, center_px, (int(end_point_px[0]), int(end_point_px[1])), 1)
                  except Exception as e: pass 