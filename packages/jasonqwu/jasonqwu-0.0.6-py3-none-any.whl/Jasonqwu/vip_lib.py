import tkinter as tk
import tkinter.messagebox
import webbrowser
import re


class VIP_APP:
    def __init__(self, width=500, height=300):
        self.w = width
        self.h = height
        self.title = ' VIP视频破解(小枫)'
        self.window = tk.Tk(className=self.title)
        # 获取URL
        self.url = tk.StringVar()

        # 播放源
        self.n = tk.IntVar()
        self.n.set(1)  # 默认1

        # Frame空间
        frame_1 = tk.Frame(self.window)
        frame_2 = tk.Frame(self.window)
        frame_3 = tk.Frame(self.window)

        # Menu菜单
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)  # 在窗口添加菜单栏
        ComboBox = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='友情链接', menu=ComboBox)  # 在菜单栏添加下拉菜单

        # 在下拉菜单添加各个网站链接
        # Lambda的使用: Lambda xx:xx 左边为定义,右边为执行语句
        ComboBox.add_command(
            label='腾讯视频',
            command=lambda: webbrowser.open('http://v.qq.com/'))
        ComboBox.add_command(
            label='搜狐视频',
            command=lambda: webbrowser.open('http://tv.sohu.com/'))
        ComboBox.add_command(
            label='芒果TV',
            command=lambda: webbrowser.open('http://www.mgtv.com/'))
        ComboBox.add_command(
            label='外挂系列-VIP视频破解',
            command=lambda: webbrowser.open('http://www.iqiyi.com/'))
        ComboBox.add_command(
            label='PPTV',
            command=lambda: webbrowser.open('http://www.bilibili.com/'))
        ComboBox.add_command(
            label='优酷',
            command=lambda: webbrowser.open('http://www.youku.com/'))
        ComboBox.add_command(
            label='乐视',
            command=lambda: webbrowser.open('http://www.le.com/'))
        ComboBox.add_command(
            label='土豆',
            command=lambda: webbrowser.open('http://www.tudou.com/'))
        ComboBox.add_command(
            label='A站',
            command=lambda: webbrowser.open('http://www.acfun.tv/'))
        ComboBox.add_command(
            label='B站',
            command=lambda: webbrowser.open('http://www.bilibili.com/'))

        # 设置控件
        # frame1
        lab = tk.Label(
            frame_1, text='请选择一个视频播放通道:',
            padx=10, pady=10)
        channel1 = tk.Radiobutton(
            frame_1, text='通道一', variable=self.n,
            value=1, width=10, height=3)
        channel2 = tk.Radiobutton(
            frame_1, text='通道二', variable=self.n,
            value=2, width=10, height=3)

        # frame_2
        lab1 = tk.Label(frame_2, text='请输入视频链接:')
        lab2 = tk.Label(frame_2, text='')
        lab3 = tk.Label(frame_2, text='')
        entry = tk.Entry(
            frame_2, textvariable=self.url,
            highlightcolor='Fuchsia', width=35)
        play = tk.Button(
            frame_2, text="播放", font=('楷体', 12),
            fg='Purple', width=2, height=1, command=self.video_play)

        # frame_3
        label_explain = tk.Label(frame_3, fg='red', font=('楷体', 12),
                                 text='\n注意：支持大部分主流视频网站的视频播放！\n')
        label_warning = tk.Label(
            frame_3, fg='blue', font=('楷体', 12),
            text='\n作者: 小枫\nQQ:1848148016')

        # 控件布局
        frame_1.pack()
        frame_2.pack()
        frame_3.pack()
        lab.grid(row=0, column=0)
        channel1.grid(row=0, column=1)
        channel2.grid(row=0, column=2)
        lab1.grid(row=0, column=0)
        lab2.grid(row=0, column=2)
        lab3.grid(row=0, column=4)
        entry.grid(row=0, column=1)
        play.grid(row=0, column=3, ipadx=10, ipady=10)
        label_explain.grid(row=1, column=0)
        label_warning.grid(row=2, column=0)

    def video_play(self):
        # 视频解析网站地址
        port_1 = 'http://www.wmxz.wang/video.php?url='
        port_2 = 'http://www.vipjiexi.com/tong.php?url='
        # 正则表达式判断url是否合法
        if re.match(r'^https?:/{2}\w.+$', self.url.get()):
            if self.n.get() == 1:
                ip = self.url.get()  # 获取视频链接
                webbrowser.open(port_1 + self.url.get())  # 浏览器打开
            elif self.n.get() == 2:
                ip = self.url.get()  # 获取视频链接
                webbrowser.open(port_2 + self.url.get())  # 浏览器打开
        else:
            tk.messagebox.showerror(title='错误', message='叼毛,地址错了！')

    def center(self):
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = int((ws / 2) - (self.w / 2))
        y = int((hs / 2) - (self.h / 2))
        self.window.geometry('{}x{}+{}+{}'.format(self.w, self.h, x, y))

    def loop(self):
        # 禁止修改窗口大小
        self.window.resizable(False, False)
        # 窗口居中
        self.center()
        self.window.mainloop()
        pass


if __name__ == '__main__':
    app = VIP_APP()
    app.loop()
