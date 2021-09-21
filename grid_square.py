import pygame
from color import BLACK, WHITE
import numpy as np

class GridSquare:
    def __init__(self, left, top, len_px, r=0, b=0, g=0):
        self.color = (r,g,b)
        self.blocked = False
        self.len_px = len_px
        self.surface = pygame.Surface((len_px, len_px))
        self.draw_rect = self.surface.get_rect()
        self.rect = pygame.Rect(left,top,len_px,len_px)
        self.font = pygame.font.SysFont('Arial', 12)
        self.draw()

    def set_rgb(self, color2):
        self.color = color2
        self.draw()

    def add_rgb(self, color2):
        self.color = [min(a+b,255) for a,b in zip(self.color,color2)]
        self.draw()

    def draw(self):
        self.surface.fill(BLACK)
        if not self.blocked:
            scaled_color = 255 * np.power((np.asarray(self.color) / 255), 1/4)
            pygame.draw.rect(self.surface, scaled_color, self.draw_rect)
            pygame.draw.rect(self.surface, WHITE, self.draw_rect, width=1)
            for i,c in enumerate(self.color):
                self.surface.blit(self.font.render(str(round(c/255,2)), False, WHITE), (self.len_px//2-10,i*10+10))
        else:
            pygame.draw.rect(self.surface, WHITE, self.draw_rect, width=0)
            pygame.draw.rect(self.surface, BLACK, self.draw_rect, width=1)
            pygame.draw.line(self.surface, BLACK, (0,0), (self.len_px,self.len_px), width=2)
            pygame.draw.line(self.surface, BLACK, (self.len_px,0), (0,self.len_px), width=2)

    def set_blocked(self, blocked):
        self.blocked = blocked
        self.set_rgb(BLACK)
        self.draw()

    def toggle_blocked(self):
        self.blocked = not self.blocked
        self.set_rgb(BLACK)
        self.draw()

    # pos should be a position relative to the grid top left
    def click(self, pos, color):
        if self.rect.collidepoint(*pos):
            if color != None:
                self.add_rgb(color)
            else:
                self.toggle_blocked()