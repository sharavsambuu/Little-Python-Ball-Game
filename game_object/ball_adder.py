import pygame
import Box2D as b2 
from   random       import randint, uniform 
from   .game_object import GameObject
from   .ball        import Ball
from   settings     import TILE_SIZE, TILE_DIM, SCREEN_WIDTH


class BallAdder(GameObject):
    ADD_INTERVAL  = 20.0 
    BALLS_PER_ADD = 4    

    def __init__(self, game_state):
        super().__init__(world=None, body_type=None)
        self.game_state = game_state
        self.clock      = 0.0
        self.clock      = - (self.ADD_INTERVAL / 2.0)

    def update(self, delta_time):
        self.clock += delta_time
        if self.clock >= self.ADD_INTERVAL:
            self.clock -= self.ADD_INTERVAL
            self._add_balls()

    def _add_balls(self):
        if not self.game_state or not self.game_state.world:
            print("Error: BallAdder cannot add balls, missing game_state or world.")
            return
        for _ in range(self.BALLS_PER_ADD):
            min_x   = TILE_SIZE * 1.5
            max_x   = (TILE_DIM[0] - 1.5) * TILE_SIZE
            spawn_x = randint(int(min_x), int(max_x))
            spawn_y = (TILE_DIM[1] - 4) * TILE_SIZE

            spawn_pos_px = (spawn_x, spawn_y)
            ball_type    = randint(0, Ball.NUM_TYPES - 1)

            new_ball = Ball(self.game_state, self.game_state.world, spawn_pos_px, ball_type)

            if new_ball.body:
                new_ball.first_thump = False
                impulse = b2.b2Vec2(uniform(-0.1, 0.1), -0.2 * new_ball.body.mass)
                new_ball.body.ApplyLinearImpulse(impulse, new_ball.body.worldCenter, True)
                self.game_state.add_game_object(new_ball)

    def draw(self, screen):
        pass 