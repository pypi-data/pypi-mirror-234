import os
import multiprocessing
import threading
from mttkinter.mtTkinter import *
from PIL import Image, ImageTk
import pyttsx3
import pygame
import turtle


def 设置窗口(主界面=False, 标题=None, 大小="1366x768", 起始="+0+0"):
    if (主界面):
        窗口 = Tk()
    else:
        窗口 = Toplevel()
    窗口.title(标题)
    窗口.geometry(大小 + 起始)
    窗口.resizable(False, False)
    return 窗口


def 设置背景(
            窗口, 大小=(1366, 768), 图片="图片/成员介绍.webp",
            relx=0, rely=0, relwidth=1, relheight=1):
    背景图片 = Image.open(os.path.join(os.path.dirname(__file__), 图片))
    背景图片 = 背景图片.resize(大小)
    背景图片 = ImageTk.PhotoImage(背景图片)
    背景标签 = Label(窗口, image=背景图片)
    背景标签.image = 背景图片
    背景标签.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return 背景标签


def 设置文本(
            窗口, text=None, font=("黑体", 20), justify="left",
            relx=0.45, rely=0.76, relwidth=0.33, relheight=0.1):

    文本标签 = Label(窗口, text=text, font=font, justify=justify)
    文本标签.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return 文本标签


def 设置输入框(
            窗口, font=("黑体", 20),
            relx=0.32, rely=0.55, relwidth=0.35, relheight=0.07):
    输入框 = Entry(窗口, font=font)
    输入框.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return 输入框


def 设置按钮(
            窗口, 图片="图片/按钮.webp", 文本=None,
            字体=("黑体", 30, "bold"), 位置="center", 命令=None,
            relx=0.4, rely=0.08, relwidth=0.22, relheight=0.06):
    按钮图片 = Image.open(os.path.join(os.path.dirname(__file__), 图片))
    按钮图片 = ImageTk.PhotoImage(按钮图片)
    按钮 = Button(窗口, image=按钮图片, text=文本, font=字体, compound=位置, command=命令)
    按钮.image = 按钮图片
    按钮.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return 按钮


def 朗读(文本=None):
    pygame.mixer.init()
    pygame.mixer.stop()
    语音模块 = pyttsx3.init()
    语音模块.save_to_file(文本, "语音.wav")
    语音模块.runAndWait()
    语音模块.stop()
    语音 = pygame.mixer.Sound("语音.wav")
    语音.play()
    try:
        os.remove("语音.wav")
    except Exception:
        print("OK!")


def 成员介绍():
    def 特斯拉(图片, 简介):
        # 任务3 = multiprocessing.Process(target=设置背景, args=[
        #     成员介绍窗口, (480, 640), 图片, 0.45, 0.1, 0.33, 0.67])
        任务3 = threading.Thread(target=设置背景, args=[
            成员介绍窗口, (480, 640), 图片, 0.45, 0.1, 0.33, 0.67])
        # 任务4 = multiprocessing.Process(target=设置文本, args=[
        #     成员介绍窗口, 特斯拉简介, ("黑体", 20), "left", 0.45, 0.76, 0.33, 0.1])
        任务4 = threading.Thread(target=设置文本, args=[
            成员介绍窗口, 特斯拉简介, ("黑体", 20), "left", 0.45, 0.76, 0.33, 0.1])
        # 任务5 = multiprocessing.Process(target=朗读, args=[特斯拉简介])
        任务5 = threading.Thread(target=朗读, args=[特斯拉简介])
        任务3.daemon = True
        任务3.start()
        任务4.daemon = True
        任务4.start()
        任务5.daemon = True
        任务5.start()

    def Guido(图片, 简介):
        # 任务6 = multiprocessing.Process(target=设置背景, args=[
        #     成员介绍窗口, (480, 640), 图片, 0.45, 0.1, 0.33, 0.67])
        任务6 = threading.Thread(target=设置背景, args=[
            成员介绍窗口, (480, 640), 图片, 0.45, 0.1, 0.33, 0.67])
        # 任务7 = multiprocessing.Process(target=设置文本, args=[
        #     成员介绍窗口, Guido简介, ("黑体", 20), "left", 0.45, 0.76, 0.33, 0.1])
        任务7 = threading.Thread(target=设置文本, args=[
            成员介绍窗口, Guido简介, ("黑体", 20), "left", 0.45, 0.76, 0.33, 0.1])
        # 任务8 = multiprocessing.Process(target=朗读, args=[Guido简介])
        任务8 = threading.Thread(target=朗读, args=[Guido简介])
        任务6.daemon = True
        任务6.start()
        任务7.daemon = True
        任务7.start()
        任务8.daemon = True
        任务8.start()

    def 退出(窗口):
        try:
            pygame.mixer.stop()
            os.remove("语音.wav")
        except Exception:
            print("OK, 退出。")
        窗口.quit()

    成员介绍窗口 = 设置窗口(标题="成员介绍")
    设置背景(成员介绍窗口, 图片="图片/成员介绍.webp")
    特斯拉简介 = "特斯拉，1856年7月10日出生，\n塞尔维亚裔美籍，接近神的男人"
    特斯拉按钮 = 设置按钮(
                成员介绍窗口, 文本="特斯拉",
                命令=lambda: 特斯拉("图片/特斯拉.webp", 特斯拉简介),
                relx=0.1, rely=0.1, relwidth=0.2, relheight=0.09)
    Guido简介 = "Guido，1956年1月31日出生，\n荷兰人，人生苦短，我用 Python"
    Guido按钮 = 设置按钮(
                成员介绍窗口, 文本="Guido",
                命令=lambda: Guido("图片/Guido.webp", Guido简介),
                relx=0.1, rely=0.2, relwidth=0.2, relheight=0.09)
    退出按钮 = 设置按钮(
                成员介绍窗口, 文本="退出",
                命令=lambda: 退出(成员介绍窗口),
                relx=0.1, rely=0.3, relwidth=0.2, relheight=0.09)


def 文字转语音():
    def 转语音():
        文本 = 输入框.get()
        朗读(文本)
        输入框.delete(0, END)

    文字转语音窗口 = 设置窗口(标题="文字转语音")
    设置背景(文字转语音窗口, 图片="图片/成员介绍.webp")
    设置文本(
        文字转语音窗口, text="请输入要转语音的文字", font=("黑体", 36),
        justify="center", relx=0.25, rely=0.36, relwidth=0.53, relheight=0.1)
    输入框 = 设置输入框(文字转语音窗口, font=("黑体", 20))
    设置按钮(
            文字转语音窗口, 文本="转 语 音", 命令=转语音,
            relx=0.4, rely=0.72, relwidth=0.2, relheight=0.09)


def 绘图():
    turtle.title("画哆啦 A 梦")
    turtle.setup(700, 500, 350, 150)
    turtle.Screen().cv._rootwindow.resizable(0, 0)
    # # turtle.bgpic(os.path.join(os.path.dirname(__file__), "图片/成员介绍.webp"))
    turtle.pensize(3)
    turtle.speed(5)
    turtle.fd(100)
    turtle.Screen().exitonclick()
    # turtle.mainloop()


def 海龟绘图():
    任务2 = multiprocessing.Process(target=绘图)
    # 任务2 = threading.Thread(target=绘图)
    任务2.daemon = True
    任务2.start()


def 首页():
    # 任务1 = multiprocessing.Process(target=朗读, args=["遇见你，好开心！"])
    任务1 = threading.Thread(target=朗读, args=["遇见你，好开心！"])
    任务1.start()
    主窗口 = 设置窗口(主界面=True, 标题="小助手")
    背景标签 = 设置背景(主窗口, 图片="图片/背景.webp")
    成员介绍按钮 = 设置按钮(主窗口, 文本="成员介绍", 命令=成员介绍)
    文字转语音按钮 = 设置按钮(主窗口, 文本="文字转语音", 命令=文字转语音, rely=0.16)
    海龟绘图按钮 = 设置按钮(主窗口, 文本="海龟绘图", 命令=海龟绘图, rely=0.24)
    # print(f"现在有{multiprocessing.active_count() - 1}个线程")
    # print(f"现在有{threading.active_count() - 1}个线程")
    主窗口.mainloop()
