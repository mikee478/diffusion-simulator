import pygame

from color import RED, GREEN, BLUE
from grid_square import GridSquare

class ChoiceSquare:
    def __init__(self, left, top, len_px):
        self.grid_sq = GridSquare(0, 0, len_px)
        self.surface = pygame.Surface((len_px, len_px))
        self.rect = self.surface.get_rect(left=left, top=top)
        self.choice = None
        self.choose_red()

    def choose_red(self):
        self.choice = RED
        self.draw()

    def choose_green(self):
        self.choice = GREEN
        self.draw()

    def choose_blue(self):
        self.choice = BLUE
        self.draw()

    def choose_blocked(self):
        self.choice = None
        self.draw()

    def draw(self):
        self.grid_sq.set_blocked(self.choice == None)

        if self.choice != None:
            self.grid_sq.set_rgb(self.choice)

        self.surface.blit(self.grid_sq.surface, self.grid_sq.rect)