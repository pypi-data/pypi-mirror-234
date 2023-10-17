# 导入pygame模块
import sys
import pygame

# 初始化pygame
pygame.init()
# 创建一个窗口
LENGTH = 760

screen = pygame.display.set_mode((LENGTH, LENGTH))
# 设置窗口标题
pygame.display.set_caption('围棋棋盘')
# 设置棋盘背景颜色
screen.fill((255, 255, 255))
# 画棋盘
for i in range(19):
    # 画横线
    pygame.draw.line(screen, (0, 0, 0), (20, 20 + 40 * i), (LENGTH - 20, 20 + 40 * i), 2)
    # 画竖线
    pygame.draw.line(screen, (0, 0, 0), (20 + 40 * i, 20), (20 + 40 * i, LENGTH -20), 2)
# 更新窗口
pygame.display.update()
# 等待操作
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
