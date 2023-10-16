#
# @author Jason Q. Wu
# @create 2021-04-21 14:19
#
import turtle as t
import random as r

def draw_circle(radius, num):
    if (radius > num):
        return
    t.pencolor(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    t.circle(radius)
    t.left(2)
    draw_circle(radius + 1, num)

def draw_polygon(color, edges):
    t.begin_fill()
    t.fillcolor(color)
    for i in range(edges):
        t.forward(20)
        t.left(180 * (edges - 1) / edges)
    t.end_fill()

def draw_rectangle(length, num):
    if (length > num):
        return
    t.pencolor(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    for i in range(4):
        t.forward(50)
        t.left(90)
    t.left(2)
    draw_rectangle(length + 1, num)

def draw_tree(pen_size, length, num):
    pen_size = pen_size * 3 / 4
    length = length * 3 / 4
    t.pensize(pen_size)
    t.pencolor(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
    t.left(45)
    t.forward(length)

    if (num < 14):
        draw_tree(pen_size, length, num + 1)

    t.backward(length)
    t.right(90)
    t.forward(length)

    if (num < 14):
        draw_tree(pen_size, length, num + 1)

    t.backward(length)
    t.left(45)
    t.pensize(pen_size)

    # for i in range(4):
    #     t.forward(50)
    #     t.left(90)
    # t.left(2)
    #

def move_to(x, y):
    t.up()
    t.goto(x, y)
    t.down()

def random_color():
    color = (r.random(), r.random(), r.random())
    return color

def random_range(min, max):
    return min + (max - min) * r.random()

def turtle_init():
    t.setup(width=1200, height=846, startx=0, starty=0)
    t.speed(0)
    t.pensize(1)
