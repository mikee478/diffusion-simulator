import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONUP, MOUSEBUTTONDOWN, K_RETURN, KEYDOWN, K_r, K_g, K_b, K_x, K_c, K_BACKSPACE
import numpy as np

from color import BLACK
from choice_square import ChoiceSquare
from controls_text import ControlsText
from grid import Grid
from grid_square import GridSquare

class DiffusionSimulation:
    def __init__(self, screen_size, n_squares, len_square):
        pygame.init()
        self.screen_size = screen_size
        self.n_squares = n_squares
        self.len_square = max(len_square, 40)

        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        self.screen.fill(BLACK)
        pygame.display.set_caption('Diffusion Simulation')

        CONTROLS_TEXT_LEFT = 4
        CONTROLS_TEXT_TOP = 1
        self.controlsText = ControlsText(CONTROLS_TEXT_LEFT, CONTROLS_TEXT_TOP)
        self.screen.blit(self.controlsText.surface, self.controlsText.rect)

        CHOICE_SQ_LEFT = (self.screen_size - self.len_square) // 2
        CHOICE_SQ_TOP = 15
        GRID_LEFT = (self.screen_size - self.len_square * self.n_squares) // 2
        GRID_TOP = max(2 * CHOICE_SQ_TOP + self.len_square, self.controlsText.rect.bottom)

        self.choice_sq = ChoiceSquare(CHOICE_SQ_LEFT, CHOICE_SQ_TOP, self.len_square)
        self.grid = Grid(GRID_LEFT, GRID_TOP, self.n_squares, self.len_square)

        self.mouse_pressed = False
        self.running = True

    def run(self):
        while self.running:

            self.grid.draw()
            self.screen.blit(self.grid.surface, self.grid.rect)
            self.screen.blit(self.choice_sq.surface, self.choice_sq.rect)

            pygame.display.flip() # Update the display

            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.grid.diffuse()
                    elif event.key == K_r:
                        self.choice_sq.choose_red()        
                    elif event.key == K_g:
                        self.choice_sq.choose_green()        
                    elif event.key == K_b:
                        self.choice_sq.choose_blue()    
                    elif event.key == K_x:
                        self.choice_sq.choose_blocked()  
                    elif event.key == K_BACKSPACE:
                        self.grid.clear_chemicals()    
                elif event.type == MOUSEBUTTONDOWN:
                    if self.choice_sq.choice == None:
                        self.grid.click(pygame.mouse.get_pos(), self.choice_sq.choice)
                    else:
                        self.mouse_pressed = True
                elif event.type == MOUSEBUTTONUP:
                    self.mouse_pressed = False

            if self.mouse_pressed:
                self.grid.click(pygame.mouse.get_pos(), self.choice_sq.choice)

        pygame.quit()

if __name__ == "__main__":
    sim = DiffusionSimulation(screen_size=625, n_squares=10, len_square=50)
    sim.run()
