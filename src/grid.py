import pygame
import numpy as np

from color import BLACK
from grid_square import GridSquare

class Grid:
    def __init__(self, left, top, n_square, len_square):
        self.surface = pygame.Surface((len_square*n_square, len_square*n_square))
        self.rect = pygame.Rect(left, top, len_square*n_square, len_square*n_square)
        self.len_square = len_square
        self.n_square = n_square
        self.grid = [[GridSquare(self.len_square*j, self.len_square*i, self.len_square) for j in range(self.n_square)] for i in range(self.n_square)]
        self.draw()

    def draw(self):
        for i,row in enumerate(self.grid):
            for j,g in enumerate(row):
                self.surface.blit(g.surface, g.rect)

    def diffuse(self):
        grid2 = [[GridSquare(self.len_square*j, self.len_square*i, self.len_square) for j in range(self.n_square)] for i in range(self.n_square)]
        delta = np.array([[1,0],[-1,0],[0,1],[0,-1],[0,0]])
        for i,row in enumerate(self.grid):
            for j,g in enumerate(row):
                if g.blocked:
                    grid2[i][j].set_blocked(True)
                else:
                    s = np.zeros(3)
                    c = 0
                    for d in delta:
                        coor = [i,j]+d
                        if np.all((coor>=0) & (coor<self.n_square)) and not self.grid[coor[0]][coor[1]].blocked:
                            s += self.grid[coor[0]][coor[1]].color
                            c += 1
                    if c != 0: 
                        s/=c
                    grid2[i][j].set_rgb(s)
        self.grid = grid2

    # Another diffusion model to fix the loss/gain of overall chemical after rounds of diffusion.
    # Doesn't evenly distribute chemical over time.
    def diffuse2(self):
        grid2 = [[GridSquare(self.len_square*j, self.len_square*i, self.len_square) for j in range(self.n_square)] for i in range(self.n_square)]
        delta = np.array([[1,0],[-1,0],[0,1],[0,-1],[0,0]])
        for i,row in enumerate(self.grid):
            for j,g in enumerate(row):
                if g.blocked:
                    grid2[i][j].set_blocked(True)
                else:
                    coors = []
                    for d in delta:
                        coor = [i,j]+d
                        if np.all((coor>=0) & (coor<self.n_square)) and not self.grid[coor[0]][coor[1]].blocked:
                            coors.append(coor)
                    c = np.asarray(self.grid[i][j].color) / len(coors)
                    for i,j in coors:
                        grid2[i][j].add_rgb(c)
        self.grid = grid2

    def click(self, screen_pos, color):
        grid_pos = (screen_pos[0]-self.rect.left, screen_pos[1]-self.rect.top)
        for i,row in enumerate(self.grid):
            for j,g in enumerate(row):
                g.click(grid_pos, color)

    def clear_chemicals(self):
        for i,row in enumerate(self.grid):
            for j,g in enumerate(row):
                g.set_rgb(BLACK)