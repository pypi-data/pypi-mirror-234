from turtle import *


goto (0, 0)
pensize(5)
y = 0
speed(0)
color("red")
bgcolor("black")
'''
for _ in range(20):
    circle(100)
    right(18)
for _ in range(5):
    setheading(90)
    goto(0, y)
    pendown()
    circle(-100, 180)
    penup()
    y -= 10
'''
penup()
x = -300
for i in range(60):
    goto(x, 0)
    pendown()
    circle(120)
    penup()
    x += 10
done()
