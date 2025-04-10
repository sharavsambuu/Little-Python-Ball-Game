import pygame
from   .game_object import GameObject
from   settings     import WHITE, BLACK


class PercentDisplay(GameObject):
    BAR_COLOR_FILLED = BLACK
    BAR_COLOR_EMPTY  = (200, 200, 200)
    BORDER_COLOR     = WHITE
    BORDER_WIDTH     = 2

    def __init__(self, position_px, dimensions_px):
        super().__init__(world=None, body_type=None)
        self.pos        = tuple(position_px)
        self.dimensions = tuple(dimensions_px)
        self.percent    = 0

        self.outer_rect = pygame.Rect(self.pos, self.dimensions)
        self.inner_rect = pygame.Rect(
            self.pos[0] + self.BORDER_WIDTH,
            self.pos[1] + self.BORDER_WIDTH,
            self.dimensions[0] - 2 * self.BORDER_WIDTH,
            self.dimensions[1] - 2 * self.BORDER_WIDTH
        )

    def update_percent(self, new_percent):
        self.percent = max(0, min(100, new_percent))

    def update(self, delta_time):
        pass 

    def draw(self, screen):
        pygame.draw.rect(screen, self.BAR_COLOR_EMPTY, self.inner_rect)

        fill_height = int(self.inner_rect.height * (self.percent / 100.0))

        if fill_height > 0:
            fill_rect = pygame.Rect(
                self.inner_rect.left,
                self.inner_rect.bottom - fill_height,
                self.inner_rect.width,
                fill_height
            )
            pygame.draw.rect(screen, self.BAR_COLOR_FILLED, fill_rect)

        pygame.draw.rect(screen, self.BORDER_COLOR, self.outer_rect, self.BORDER_WIDTH)