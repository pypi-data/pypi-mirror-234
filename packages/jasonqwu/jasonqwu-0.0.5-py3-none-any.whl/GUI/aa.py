from PySide6.QtWidgets import QApplication, QMainWindow, QLabel


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        btn = QLabel("来点点我呀！", self)
        # btn.setGeometry(0, 0, 200, 100)
        # btn.setToolTip("点我有惊喜！")
        # btn.setText("换了换了")


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
