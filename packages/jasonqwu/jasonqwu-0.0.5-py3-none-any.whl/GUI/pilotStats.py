import ipdb
from PySide6.QtWidgets import QApplication, QMainWindow
# , QPushButton, QPlainTextEdit, QMessageBox
# from PySide6.QtWidgets import QApplication #, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
# from threading import Thread

class Stats:
    def __init__(self, file=None):
        if file != None:
            # 从文件中加载 UI 定义
            self.file = QFile(file)
            self.file.open(QFile.ReadOnly)
            self.file.close()

            # 从文件中加载UI定义
            # 从 UI 定义中动态创建一个相应的窗口对象
            # 注意：里面的控件对象也成为窗口对象的属性了
            # 比如：self.ui.button, self.ui.text
            self.ui = QUiLoader().load(file)
            self.ui.setWindowTitle('海运数据爬取分析')
        else:
            self.ui = QMainWindow()

def main():
    # ipdb.set_trace()
    app = QApplication([])
    stats = Stats('window.ui')
    stats.ui.show()
    app.exec()

if __name__ == '__main__':
    main()
