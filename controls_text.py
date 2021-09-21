import pygame
from color import WHITE

class ControlsText:
	def __init__(self, left, top, text_strs):
		self.text_strs = text_strs
		self.font = pygame.font.SysFont('Arial', 12)

		self.vert_offset_px = 12
		text_width, text_height = self.font.size(max(text_strs, key=len))
		self.surface = pygame.Surface((text_width, text_height*len(self.text_strs)))
		self.rect = self.surface.get_rect(left=left,top=top)
		self.draw()

	def draw(self):
		for i,s in enumerate(self.text_strs):
			self.surface.blit(self.font.render(s, False, WHITE), (0,i*self.vert_offset_px))