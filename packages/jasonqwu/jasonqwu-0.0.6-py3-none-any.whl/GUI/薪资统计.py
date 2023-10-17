'''
薛蟠        4560    25
薛蝌        4460    25
薛宝钗    35776    23
薛宝琴    14346    18
王夫人    43360    45
王熙凤    24460    25
王子腾    55660    45
王仁        15034    65
尤二姐    5324    24
贾芹        5663    25
贾兰        13443    35
贾芸        4522    25
尤三姐    5905    22
贾珍        54603    35
'''
import ipdb
import sys
from PySide6.QtWidgets import QApplication, \
    QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
import requests


class Window:
    def __init__(self, file=None):
        if file:
            # 从文件中加载 UI 定义
            self.file = QFile(file)
            self.file.open(QFile.ReadOnly)
            self.file.close()

            # 从 UI 定义中动态创建一个相应的窗口对象
            # 注意：里面的控件对象也成为窗口对象的属性了
            # 比如：self.ui.button, self.ui.text
            self.window = QUiLoader().load(file)
        else:
            self.window = QMainWindow()

    def show(self):
        self.window.show()


class 薪资统计(Window):
    def __init__(self, file=None):
        super().__init__(file)
        self.window.button.clicked.connect(self.calculate)

    def set(self, width, height, x, y, title=""):
        self.window.setWindowTitle(title)
        self.window.resize(width, height)
        self.window.move(x, y)

    def text(self, width, height, x, y, prompt=""):
        self.window.text = QPlainTextEdit(self.window)
        self.window.text.setPlaceholderText(prompt)
        self.window.text.resize(width, height)
        self.window.text.move(x, y)

    def button(self, x, y, title=""):
        self.window.button = QPushButton(title, self.window)
        self.window.button.move(x, y)

    def clicked(self, func):
        self.window.button.clicked.connect(func)

    def calculate(self):
        print("统计按钮被点击了。")
        info = self.window.text.toPlainText()

        # 薪资 20000 以上和以下的人员名单
        salary_above_20k = "\n"
        salary_below_20k = "\n"
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split('\t')
            # ipdb.set_trace()

            # 去掉列表中的空字符串内容
            parts = [p for p in parts if p]
            print(f"{parts}")
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(
            self.window,
            "统计结果",
            f'''薪资 20000 以上的有：
            {salary_above_20k}
            薪资 20000 以下的有：
            {salary_below_20k}'''
        )


class 黑羽数据管理(Window):
    def __init__(self, file=None):
        super().__init__(file)


class Login(Window):
    def __init__(self, file=None):
        super().__init__(file)
        self.window.btn_login.clicked.connect(self.login)
        self.window.edt_password.returnPressed.connect(self.login)

    def login(self):
        username = self.window.edt_username.text().strip()
        password = self.window.edt_password.text().strip()
        s = requests.Session()


def run_薪资统计():
    # QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts);
    # QCoreApplication.setAttribute(Qt.AA_UseOpenGLES);
    # QQuickWindow.setGraphicsApi(QSGRendererInterface.OpenGLRhi)
    app = QApplication([])
    app.setWindowIcon(QIcon("resources/Icon/Jason.png"))
    window = 薪资统计("resources/UI/薪资统计.ui")

    # ipdb.set_trace()
    # window = 薪资统计()
    # window.set(500, 400, 300, 300, "薪资统计")
    # window.text(300, 350, 10, 25, "请输入薪资信息")
    # window.button(380, 80, "统计")
    # window.clicked(window.calculate)

    window.show()
    sys.exit(app.exec())


def run_黑羽数据管理():
    app = QApplication([])
    app.setWindowIcon(QIcon("resources/Icon/Jason.png"))
    window = 黑羽数据管理("resources/UI/黑羽数据管理.ui")
    window.show()
    sys.exit(app.exec())


def run_login():
    app = QApplication([])
    app.setWindowIcon(QIcon("resources/Icon/Jason.png"))
    window = Login("resources/UI/登录.ui")
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_薪资统计()
    run_黑羽数据管理()
    run_login()

'''test window_lib'''
# import window_lib

# window_lib.run_薪资统计()
# window_lib.run_黑羽数据管理()
# window_lib.run_login()
