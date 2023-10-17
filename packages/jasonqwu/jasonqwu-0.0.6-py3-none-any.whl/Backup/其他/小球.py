import pygame
import random

# 设置背景颜色和线条颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Ball:
	def __init__(self, x=0, y=0, radius=25, speed_x=0.2, speed_y=0.2):
		self.x = x
		self.y = y
		self.radius = radius
		self.speed_x = speed_x
		self.speed_y = speed_y

	def draw(self, screen=None, color=WHITE, pen_width=0):
		width, height = pygame.display.get_surface().get_size()
		if self.x <= self.radius or self.x >= width - self.radius:
			self.speed_x = -self.speed_x
		if self.y <= self.radius or self.y >= height - self.radius:
			self.speed_y = -self.speed_y
		self.x += self.speed_x
		self.y += self.speed_y
		pygame.draw.circle(screen, color, (self.x, self.y), self.radius, pen_width)

pygame.init()
width = 1200
height = 600
x = width // 2
y = height // 2
radius = 25
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("一个小球")
ball = []
amount = random.randint(5, 15)
for i in range(amount):
	radius = random.randint(5, 40)
	speed_x = random.random()
	speed_y = random.random()
	ball.append(Ball(random.randint(radius, width - radius), random.randint(radius, height - radius), radius, speed_x, speed_y))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill(BLACK)
    for i in range(amount):
	    ball[i].draw(screen, WHITE, 0)
    pygame.display.update()
