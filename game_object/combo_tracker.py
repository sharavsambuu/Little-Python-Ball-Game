import pygame
from   .game_object import GameObject


class ComboTracker(GameObject):
    """Tracks consecutive ball pops to award combo points."""
    COMBO_WINDOW       = 2.5
    MIN_POPS_FOR_COMBO = 3
    COMBO_BONUS_POINTS = 4

    def __init__(self, game_state):
        super().__init__(world=None, body_type=None)
        self.game_state          = game_state
        self.time_since_last_pop = self.COMBO_WINDOW + 1.0
        self.combo_count         = 0
        try:
            self.combo_sound = pygame.mixer.Sound('data/sound/fx/boom.ogg')
            self.combo_sound.set_volume(0.7)
        except pygame.error as e:
            print(f"Warning: Could not load combo sound: {e}")
            self.combo_sound = None

    def record_pop(self):
        if self.time_since_last_pop <= self.COMBO_WINDOW:
            self.combo_count += 1
        else:
            self.combo_count = 1 

        if self.combo_count >= self.MIN_POPS_FOR_COMBO:
            if self.game_state:
                self.game_state.add_score(self.COMBO_BONUS_POINTS)
            if self.combo_sound:
                self.combo_sound.play()
            # print(f"COMBO! +{self.COMBO_BONUS_POINTS} points (Count: {self.combo_count})")

        self.time_since_last_pop = 0.0

    def update(self, delta_time):
        self.time_since_last_pop += delta_time

    def draw(self, screen):
        pass 