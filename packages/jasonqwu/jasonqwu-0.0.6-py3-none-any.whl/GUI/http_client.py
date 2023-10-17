import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_http_client import Ui_http_client
import logging_lib


log = logging_lib.Logger("log0")


class Window(QMainWindow):
    def __init__(self):
        # 加载 Ui_window 定义
        super(Window, self).__init__()
        self.ui = Ui_http_client()
        self.ui.setupUi(self)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
    sys.exit()


if __name__ == '__main__':
    main()
