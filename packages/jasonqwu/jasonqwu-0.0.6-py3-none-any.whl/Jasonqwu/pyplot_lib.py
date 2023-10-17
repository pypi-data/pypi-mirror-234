#
# @author Jason Q. Wu
# @create 2021-04-22 9:23
#
import matplotlib.pyplot as plt
import numpy as np

def bar_chart(title, city, p1, p2, bar_width):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(title)
    plt.bar(range(len(city)), p1, color = "steelblue", width = bar_width, label = "确诊人数")
    plt.bar(np.arange(len(city)) + bar_width + 0.005, p2, color = "indianred", width = bar_width, label = "治愈人数")
    for x, y in enumerate(p1):
        plt.text(x, y + 5, str(y), ha = "center", va = "bottom")
    for x, y in enumerate(p2):
        plt.text(x + bar_width + 0.005, y + 5, str(y), ha = "center", va = "bottom")
    plt.legend()
    plt.show()

def line_chart(x, y1 = None, y2 = None, y3 = None, y4 = None, y_label = "人数"):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    if y1 != None:
        plt.plot(x[1:], y1[1:], "yo-", label = y1[0])
    if y2 != None:
        plt.plot(x[1:], y2[1:], "bo-", label = y2[0])
    if y3 != None:
        plt.plot(x[1:], y3[1:], "go-", label = y3[0])
    if y4 != None:
        plt.plot(x[1:], y4[1:], "ro-", label = y4[0])
    plt.xlabel(x[0])
    plt.ylabel(y_label)
    plt.legend()
    plt.show()

def pie_chart(data, city, el):
    plt.pie(data, labels = city, autopct = '%.2f%%', explode = el, shadow = True)
    plt.show()