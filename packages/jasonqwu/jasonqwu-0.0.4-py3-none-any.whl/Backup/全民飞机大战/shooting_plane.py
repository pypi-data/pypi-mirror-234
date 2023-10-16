import random
import pygame
from plane_sprites import *

class PlaneGame(object):
	"""飞机大战主游戏"""
	def __init__(self):
		print("游戏初始化......")
		pygame.init()
		# 创建游戏的窗口
		self.screen = pygame.display.set_mode(SCREEN_RECT.size)
		# 设置窗口的标题和图标
		pygame.display.set_caption("飞机大战")
		icon = pygame.image.load("./image/aircraft_image/plane.png")
		pygame.display.set_icon(icon)

		# 创建游戏的时钟
		self.clock = pygame.time.Clock()
		# 创建精灵和精灵组
		self.__create_sprites()
		# 创建定时器事件
		pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
		pygame.time.set_timer(HERO_FIRE_EVENT, 500)

	def __create_sprites(self):
		# 创建背景的精灵组
		picture = random.randint(1, 5)
		self.bg1 = Background(picture)
		self.bg2 = Background(picture, True)
		self.back_group = pygame.sprite.Group(self.bg1, self.bg2)
		# 创建敌机的精灵组
		self.enemy_group = pygame.sprite.Group()
		# 创建英雄的精灵组
		picture = random.randint(1, 3)
		self.hero = Hero(picture)
		self.hero_group = pygame.sprite.Group(self.hero)

	def __event_handler(self):
		for event in pygame.event.get():
			# 判断是否退出游戏
			if event.type == pygame.QUIT:
				self.__game_over()
			elif event.type == CREATE_ENEMY_EVENT:
				# print("敌机出场......")
				# 创建敌机精灵
				enemy = Enemy()
				# 添加到敌机精灵组
				self.enemy_group.add(enemy)
			elif event.type == HERO_FIRE_EVENT:
				self.hero.fire()

		# 通过键盘函数获取键盘按键
		keys_pressed = pygame.key.get_pressed()
		# 通过元组判断按键
		if keys_pressed[pygame.K_LEFT]:
			print("向左移动......")
			self.hero.speed += -1;
		elif keys_pressed[pygame.K_RIGHT]:
			print("向右移动......")
			self.hero.speed += 1;
		else:
			self.hero.speed = 0;

	def __check_collide(self):
		# 子弹摧毁敌机
		pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)
		# 英雄牺牲
		enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
		# 判断列表是否有内容
		if len(enemies) > 0:
			self.hero.kill()
			self.__game_over()

	def __update_sprites(self):
		self.back_group.update()
		self.back_group.draw(self.screen)
		self.hero_group.update()
		self.hero_group.draw(self.screen)
		self.hero.bullet_group.update()
		self.hero.bullet_group.draw(self.screen)
		self.enemy_group.update()
		self.enemy_group.draw(self.screen)

	@staticmethod
	def __game_over():
		print("游戏结束......")
		pygame.quit()
		exit()

	def start_game(self):
		print("游戏开始......")
		bg_rect = pygame.Rect(0, 0, SCREEN_RECT.x, SCREEN_RECT.y)
		hero_rect = pygame.Rect(TOP_X, TOP_Y, WIDTH, HEIGHT)

		while True:
			# 设置刷新帧率
			self.clock.tick(FRAME_PER_SECOND)
			# 事件监听
			self.__event_handler()
			# 碰撞检测
			self.__check_collide()
			# 更新精灵组
			self.__update_sprites()
			pygame.display.update()

if __name__ == '__main__':
	game = PlaneGame()
	game.start_game()
