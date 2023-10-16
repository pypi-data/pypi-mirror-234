import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 512, 700)
# 窗口的坐标设置
TOP_X = 200
TOP_Y = 550
WIDTH = 124
HEIGHT = 104
# 刷新的帧率常量
FRAME_PER_SECOND = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 发射子弹的定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
	"""飞机大战游戏精灵组"""
	def __init__(self, image_name, speed=1):
		# 调用父类的初始化方法
		super().__init__()
		# 定义对象的属性
		self.image = pygame.image.load(image_name)
		self.rect = self.image.get_rect()
		self.speed = speed

	def update(self):
		self.rect.y += self.speed

class Background(GameSprite):
	"""背景精灵组"""
	def __init__(self, picture=1, is_alt=False):
		# 选用随机的背景图片进行初始化
		if picture == 1:
			super().__init__("./image/aircraft_image/image_1.jpg")
		elif picture == 2:
			super().__init__("./image/aircraft_image/image_2.jpg")
		elif picture == 3:
			super().__init__("./image/aircraft_image/image_3.jpg")
		elif picture == 4:
			super().__init__("./image/aircraft_image/image_4.jpg")
		else:
			super().__init__("./image/aircraft_image/image_5.jpg")
		# 背景图片走出窗口后放到上面可以继续移动
		if is_alt:
			self.rect.y = -self.rect.height

	def update(self):
		super().update()
		if self.rect.y >= SCREEN_RECT.height:
			self.rect.y = -self.rect.height

class Hero(GameSprite):
	"""英雄精灵"""
	def __init__(self, picture):
		# 调用父类方法，设置图片和速度
		if picture == 1:
			super().__init__("./image/aircraft_image/main_1.png", 0)
		elif picture == 2:
			super().__init__("./image/aircraft_image/main_2.png", 0)
		else:
			super().__init__("./image/aircraft_image/main_3.png", 0)
		# 设置英雄的初始位置
		self.rect.centerx = SCREEN_RECT.centerx
		self.rect.bottom = SCREEN_RECT.bottom - 10
		# 创建子弹的精灵组
		self.bullet_group = pygame.sprite.Group()

	def update(self):
		self.rect.x += self.speed
		if self.rect.x < 0:
			self.rect.x = 0
		if self.rect.right > SCREEN_RECT.right:
			self.rect.right = SCREEN_RECT.right

	def fire(self):
		print("发射子弹......")

		# for i in (0, 1, 2):
		# 创建子弹精灵
		self.bullet = Bullet()
		# 设置初始位置
		self.bullet.rect.centerx = self.rect.centerx
		self.bullet.rect.bottom = self.rect.top
		# 将子弹添加到精灵组
		self.bullet_group.add(self.bullet)

class Bullet(GameSprite):
	"""子弹精灵"""
	def __init__(self):
		# 调用父类方法，设置子弹图片，设置初始速度
		super().__init__("./image/aircraft_image/mybollet1.png", -1)
		# super().__init__("./image/aircraft_image/mybuttle.png", -1)
		# super().__init__("./image/aircraft_image/mybollet3.png", -1)

	def update(self):
		# 调用父类方法，让子弹沿垂直方向飞行
		super().update()
		# 判断子弹是否飞出屏幕
		if self.rect.bottom < 0:
			self.kill()

	def __del__(self):
		print("子弹被销毁......")

class Enemy(GameSprite):
	"""敌机精灵组"""
	def __init__(self):
		# 创建敌机精灵，指定敌机的随机图片
		picture = random.randint(1, 3)
		if picture == 1:
			super().__init__("./image/aircraft_image/small_n1.png")
		elif picture == 2:
			super().__init__("./image/aircraft_image/small_n2.png")
		else:
			super().__init__("./image/aircraft_image/small_n3.png")
		# 指定敌机的初始随机速度
		self.speed = random.randint(1, 3)
		# 指定敌机的初始随机位置
		self.rect.bottom = 0
		max_x = SCREEN_RECT.width - self.rect.width
		self.rect.x = random.randint(0, max_x)

	def update(self):
		# 调用父类方法，保持垂直方向的飞行
		super().update()
		# 判断是否飞出屏幕，如果是，需要删除敌机
		if self.rect.y >= SCREEN_RECT.height:
			# print("飞出屏幕，需要删除敌机......")
			# 将精灵从精灵组删除
			self.kill()

	def __del__(self):
		# print("敌机挂了 %s" % self.rect)
		pass
