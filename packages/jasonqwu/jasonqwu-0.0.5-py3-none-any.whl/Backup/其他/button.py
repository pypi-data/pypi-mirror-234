import pygame

class Button:
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface, color=BLACK):
		action = False
		pygame.draw.rect(surface, color, (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
		bk = pygame.draw.rect(surface, WHITE, (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()), 3)
		pos = pygame.mouse.get_pos()
