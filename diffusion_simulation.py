import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONUP, K_RETURN, KEYDOWN, K_r, K_g, K_b, K_x, K_c, K_BACKSPACE
import numpy as np

class ChoiceSquare:
    def __init__(self, left, top, len_px):
        self.grid_sq = GridSquare(0, 0, len_px)
        self.surface = pygame.Surface((len_px, len_px))
        self.rect = self.surface.get_rect(left=left,top=top)
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

class GridSquare:
    def __init__(self, left, top, len_px, r=0, b=0, g=0):
        self.color = (r,g,b)
        self.blocked = False
        self.len_px = len_px
        self.surface = pygame.Surface((len_px, len_px))
        self.draw_rect = self.surface.get_rect()
        self.rect = pygame.Rect(left,top,len_px,len_px)
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
            pygame.draw.rect(self.surface, self.color, self.draw_rect)
            pygame.draw.rect(self.surface, WHITE, self.draw_rect, width=1)
            for i,c in enumerate(self.color):
                self.surface.blit(FONT.render(str(round(c/255,2)), False, WHITE), (self.len_px//2-10,i*10+10))
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

class Grid:
    def __init__(self, left, top, len_square, n_square):
        self.left = left
        self.top = top
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

    def click(self, screen_pos, color):
        grid_pos = (screen_pos[0]-self.left, screen_pos[1]-self.top)
        for i,row in enumerate(self.grid):
            for j,g in enumerate(row):
                if g.rect.collidepoint(*grid_pos):
                    if color != None:
                        g.add_rgb(color)
                    else:
                        g.toggle_blocked()

    def clear_chemicals(self):
        for i,row in enumerate(self.grid):
            for j,g in enumerate(row):
                g.set_rgb(BLACK)

SCREEN_SIZE = 600
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
FONT = pygame.font.SysFont('Arial', 12)
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
screen.fill(BLACK)
pygame.display.set_caption('Diffusion Simulation')
clock = pygame.time.Clock()
running = True

LEN_SQUARE = 50
N_SQUARES = 10
grid = Grid(50, 75, LEN_SQUARE, N_SQUARES)
choice_sq = ChoiceSquare((SCREEN_SIZE - LEN_SQUARE)//2, 12, LEN_SQUARE)

TEXT_LEFT = 3
TEXT_TOP = 0
TEXT_STRS = ["R = Red", "G = Green", "B = Blue", "X = Blocked", "Enter = Diffuse", "Backspace = Clear Chemicals"]
for i,s in enumerate(TEXT_STRS):
    screen.blit(FONT.render(s, False, WHITE), (TEXT_LEFT,TEXT_TOP+i*12))

while running:

    grid.draw()
    screen.blit(grid.surface, grid.rect)
    screen.blit(choice_sq.surface, choice_sq.rect)

    pygame.display.flip() # Update the display

    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                grid.diffuse()
            elif event.key == K_r:
                choice_sq.choose_red()        
            elif event.key == K_g:
                choice_sq.choose_green()        
            elif event.key == K_b:
                choice_sq.choose_blue()    
            elif event.key == K_x:
                choice_sq.choose_blocked()  
            elif event.key == K_BACKSPACE:
                grid.clear_chemicals()    
        elif event.type == MOUSEBUTTONUP: 
            grid.click(pygame.mouse.get_pos(), choice_sq.choice)

pygame.quit() 