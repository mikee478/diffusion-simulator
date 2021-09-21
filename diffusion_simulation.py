import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONUP, K_RETURN, KEYDOWN, K_r, K_g, K_b, K_x, K_c, K_BACKSPACE
import numpy as np

from color import BLACK
from config import SCREEN_SIZE, LEN_SQUARE, N_SQUARES, CONTROLS_TEXT_LEFT, CONTROLS_TEXT_TOP, CONTROLS_TEXT_STRS
from choice_square import ChoiceSquare
from controls_text import ControlsText
from grid import Grid
from grid_square import GridSquare

class DiffusionSimulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.screen.fill(BLACK)
        pygame.display.set_caption('Diffusion Simulation')

        self.grid = Grid(50, 75, LEN_SQUARE, N_SQUARES)
        self.choice_sq = ChoiceSquare((SCREEN_SIZE - LEN_SQUARE)//2, 12, LEN_SQUARE)

        self.controlsText = ControlsText(CONTROLS_TEXT_LEFT, CONTROLS_TEXT_TOP, CONTROLS_TEXT_STRS)
        self.screen.blit(self.controlsText.surface, self.controlsText.rect)

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
                elif event.type == MOUSEBUTTONUP: 
                    self.grid.click(pygame.mouse.get_pos(), self.choice_sq.choice)

        pygame.quit() 

if __name__ == "__main__":
    sim = DiffusionSimulation()
    sim.run()