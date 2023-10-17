import turtle as t
import random

(r, g, b) = (0, 0, 0)
t.pensize(3)
t.speed(100)
t.penup()
t.goto(0, 0)
t.pendown()
t.bgcolor("black")
t.tracer(False)
for _ in range(360):
    r = random.random()
    g = random.random()
    b = random.random()
    t.pencolor(r, g, b)
    t.forward(200)
    t.backward(200)
    t.right(1)
t.done()
